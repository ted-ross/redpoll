/*
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 *
 */

#include <proton/connection.h>
#include <proton/condition.h>
#include <proton/delivery.h>
#include <proton/link.h>
#include <proton/message.h>
#include <proton/proactor.h>
#include <proton/session.h>
#include <proton/transport.h>

#include "ctools.h"

#include <stdio.h>
#include <stdlib.h>


typedef struct link_ref_t {
    DEQ_LINKS(struct link_ref_t);
    pn_link_t *link;
} link_ref_t;

DEQ_DECLARE(link_ref_t, link_ref_list_t);


typedef struct lock_t {
    DEQ_LINKS(struct lock_t);
    char            *name;
    pn_link_t       *current_link;
    link_ref_list_t  waiting_links;
} lock_t;

DEQ_DECLARE(lock_t, lock_list_t);


typedef struct app_data_t {
    const char      *host;
    const char      *port;
    const char      *container_id;
    const char      *prefix;
    pn_proactor_t   *proactor;
    pn_connection_t *conn;
    pn_session_t    *sess;
    pn_link_t       *sender;
    pn_link_t       *receiver;
    const char      *reply_to;
    lock_list_t      locks;
} app_data_t;


static lock_t *rpls_find_lock(app_data_t *app, const char *name)
{
    lock_t *lock = DEQ_HEAD(app->locks);

    while (lock && strcmp(lock->name, name))
        lock = DEQ_NEXT(lock);

    if (!lock) {
        //printf("Creating new lock: %s\n", name);
        lock = NEW(lock_t);
        ZERO(lock);
        lock->name = (char*) malloc(strlen(name) + 1);
        strcpy(lock->name, name);
        DEQ_INSERT_TAIL(app->locks, lock);
    }

    return lock;
}


static void rpls_add_link(lock_t *lock, pn_link_t *link)
{
    link_ref_t *ref = NEW(link_ref_t);
    ZERO(ref);
    ref->link = link;
    pn_link_set_context(link, (void*) ref);
    DEQ_INSERT_TAIL(lock->waiting_links, ref);
}


static bool rpls_link_attached(app_data_t *app, pn_link_t *link, const char *name)
{
    lock_t *lock = rpls_find_lock(app, name);

    if (!lock->current_link) {
        //printf("Lock acquired: %s\n", name);
        lock->current_link = link;
        return true;
    } else {
        //printf("Lock deferred: %s\n", name);
        rpls_add_link(lock, link);
    }

    return false;
}


static pn_link_t *rpls_get_next_link(lock_t *lock)
{
    link_ref_t *ref = DEQ_HEAD(lock->waiting_links);
    if (ref) {
        DEQ_REMOVE_HEAD(lock->waiting_links);
        pn_link_t *link = ref->link;
        pn_link_set_context(link, 0);
        free(ref);
        return link;
    }

    return 0;
}


static void rpls_remove_link(lock_t *lock, pn_link_t *link)
{
    link_ref_t *ref = (link_ref_t*) pn_link_get_context(link);
    if (ref) {
        DEQ_REMOVE(lock->waiting_links, ref);
        pn_link_set_context(link, 0);
        free(ref);
    }
}


static pn_link_t *rpls_link_detached(app_data_t *app, pn_link_t *link, const char *name)
{
    lock_t *lock = rpls_find_lock(app, name);

    if (lock->current_link == link) {
        lock->current_link = rpls_get_next_link(lock);
        //printf("Lock %s: %s\n", lock->current_link ? "transferred" : "released", name);
        return lock->current_link;
    }

    rpls_remove_link(lock, link);
    return 0;
}


static pn_bytes_t rpls_bytes(const char *value)
{
    return pn_bytes(strlen(value), value);
}


static void rpls_send_link_route_create(app_data_t* app)
{
    pn_message_t *msg  = pn_message();
    pn_data_t    *body = pn_message_body(msg);
    pn_data_t    *ap   = pn_message_properties(msg);

    pn_message_set_reply_to(msg, app->reply_to);

    //
    // Set up the application properties map
    //
    pn_data_put_map(ap);
    pn_data_enter(ap);

    pn_data_put_symbol(ap, rpls_bytes("operation"));
    pn_data_put_string(ap, rpls_bytes("CREATE"));

    pn_data_put_symbol(ap, rpls_bytes("type"));
    pn_data_put_string(ap, rpls_bytes("org.apache.qpid.dispatch.router.connection.attachSubscription"));

    pn_data_put_symbol(ap, rpls_bytes("name"));
    pn_data_put_string(ap, rpls_bytes("mutex.#"));

    pn_data_exit(ap);

    //
    // Set up the body map
    //
    pn_data_put_map(body);
    pn_data_enter(body);

    pn_data_put_symbol(body, rpls_bytes("pattern"));
    pn_data_put_string(body, rpls_bytes("mutex.#"));

    pn_data_put_symbol(body, rpls_bytes("direction"));
    pn_data_put_string(body, rpls_bytes("out"));

    pn_data_exit(body);

    //
    // Send the request
    //
    char           bytes[1000];
    size_t         size = 1000;
    pn_delivery_t *dlv  = pn_delivery(app->sender, pn_dtag("00", 2));

    pn_message_encode(msg, bytes, &size);
    ssize_t result = pn_link_send(app->sender, bytes, size);
    pn_link_advance(app->sender);
 }


/* Returns true to continue, false if finished */
static bool handle(app_data_t* app, pn_event_t* event)
{
    switch (pn_event_type(event)) {

    case PN_CONNECTION_INIT: {
        app->conn = pn_event_connection(event);
        pn_connection_set_container(app->conn, app->container_id);
        pn_connection_set_hostname(app->conn, app->host);
        pn_connection_open(app->conn);
        break;
    }

    case PN_CONNECTION_REMOTE_OPEN:
        app->sess = pn_session(app->conn);
        pn_session_open(app->sess);

        app->receiver = pn_receiver(app->sess, "lock_service_receiver");
        pn_terminus_set_dynamic(pn_link_source(app->receiver), true);
        pn_link_open(app->receiver);
        break;

    case PN_TRANSPORT_CLOSED:
        break;

    case PN_CONNECTION_REMOTE_CLOSE:
        break;

    case PN_SESSION_REMOTE_OPEN: {
        pn_session_t *session = pn_event_session(event);
        pn_session_open(session);
        break;
    }

    case PN_SESSION_REMOTE_CLOSE: {
        pn_session_t *session = pn_event_session(event);
        pn_session_close(session);
        break;
    }

    case PN_LINK_REMOTE_OPEN: {
        pn_link_t *link = pn_event_link(event);

        //
        // If the link is our management sender, send the connection link-route setup
        //
        if (link == app->sender) {
            rpls_send_link_route_create(app);
            break;
        }

        //
        // If the link is our dynamic receiver, get the address and set up the management sender
        //
        if (link == app->receiver) {
            app->reply_to = pn_terminus_get_address(pn_link_remote_source(link));

            app->sender = pn_sender(app->sess, "lock_service_sender");
            pn_terminus_set_address(pn_link_target(app->sender), "$management");
            pn_link_open(app->sender);

            pn_link_flow(app->receiver, 10);
            break;
        }

        //
        // If the link is not a sender, close it.
        //
        if (pn_link_is_receiver(link)) {
            pn_link_close(link);
            break;
        }

        //
        // Get the remote source.  Close links with no source address.
        //
        pn_terminus_t *source = pn_link_remote_source(link);
        const char    *addr   = source ? pn_terminus_get_address(source) : 0;
        if (!addr) {
            pn_link_close(link);
            break;
        }

        bool open = rpls_link_attached(app, link, addr);
        if (open) {
            pn_terminus_set_address(pn_link_source(link), addr);
            pn_link_open(link);
        }
        break;
    }

    case PN_LINK_REMOTE_CLOSE:
    case PN_LINK_REMOTE_DETACH: {
        pn_link_t     *link   = pn_event_link(event);
        pn_terminus_t *source = pn_link_remote_source(link);
        const char    *addr   = source ? pn_terminus_get_address(source) : 0;

        if (addr) {
            pn_link_t *next_link = rpls_link_detached(app, link, addr);
            if (next_link) {
                pn_terminus_set_address(pn_link_source(next_link), addr);
                pn_link_open(next_link);
            }
        }

        pn_link_close(link);
        break;
    }

    case PN_PROACTOR_INACTIVE:
        return false;

    default:
        break;
    }

    return true;
}


void run(app_data_t *app)
{
    /* Loop and handle events */
    do {
        pn_event_batch_t *events = pn_proactor_wait(app->proactor);
        for (pn_event_t *e = pn_event_batch_next(events); e; e = pn_event_batch_next(events)) {
            if (!handle(app, e)) {
                return;
            }
        }
        pn_proactor_done(app->proactor, events);
    } while (true);
}


int main(int argc, char **argv)
{
    app_data_t *app = NEW(app_data_t);
    ZERO(app);

    int i = 0;
    app->container_id = argv[i++];   /* Should be unique */
    app->host         = (argc > i) ? argv[i++] : "127.0.0.1";
    app->port         = (argc > i) ? argv[i++] : "amqp";
    app->prefix       = (argc > i) ? argv[i++] : "mutex.#";

    app->proactor = pn_proactor();
    char addr[PN_MAX_ADDR];
    pn_proactor_addr(addr, sizeof(addr), app->host, app->port);
    pn_proactor_connect(app->proactor, pn_connection(), addr);
    run(app);
    pn_proactor_free(app->proactor);
}
