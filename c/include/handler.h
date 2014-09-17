//
// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.
//

#include <proton/event.h>
#include <proton/connection.h>
#include <proton/session.h>
#include <proton/link.h>
#include <proton/delivery.h>

typedef void (*rp_event_handler_t)(void *context, pn_event_t *event);

typedef rp_handler_t rp_handler_t;

void rp_initialize();
void rp_finalize();
pn_connection_t *rp_connection();

rp_handler_t *rp_add_global_handler(pn_event_type_t et, rp_event_handler_t handler, void *context);
rp_handler_t *rp_add_connection_handler(pn_connection_t *conn, pn_event_type_t et, rp_event_handler_t handler, void *context);
rp_handler_t *rp_add_session_handler(pn_session_t *sess, pn_event_type_t et, rp_event_handler_t handler, void *context);
rp_handler_t *rp_add_link_handler(pn_link_t *link, pn_event_type_t et, rp_event_handler_t handler, void *context);
rp_handler_t *rp_add_delivery_handler(pn_delivery_t *dlv, pn_event_type_t et, rp_event_handler_t handler, void *context);
void rp_del_handler(rp_handler_t *handler);

