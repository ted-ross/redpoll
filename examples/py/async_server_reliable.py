#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from redpoll import Connection, Receiver, Sender, SENDER_REQUIRE_ACK, RECEIVER_EXACTLY_ONCE, ACCEPT

HOST  = "localhost:5672"
DEST  = "destination"

class Request(object):
    """
    This class tracks a single request through completion, when the response
    message is either accepted or rejected by the requestor.
    """
    def __init__(self, request, response, server):
        self.request  = request
        self.response = response
        self.server   = server

    def on_accept(self, link, msg):
        self.server.response_link.accept(self.request)

    def on_reject(self, link, msg):
        self.server.response_link.reject(self.request)


class Server(object):
    """
    This class is the server application and it handles incoming messages from an
    incoming request link.  There is only one instance of this class created.
    """
    def __init__(self, conn):
        self.conn = conn
        self.request_link  = Receiver(self.conn, DEST, handler=self, delivery_mode=RECEIVER_EXACTLY_ONCE)
        self.response_link = Sender(self.conn, delivery_mode=SENDER_REQUIRE_ACK)

    def run(self):
        self.conn.run()

    def on_message(self, link, msg):
        response = Message(msg.body)
        response.addr = msg.reply_to
        req = Request(msg, response, self)
        self.response_link.send(msg, handler=req)
        ##
        ## Note that this handler does not accept the message.  This is deferred
        ## until after the response is completed.
        ##

##
## Create a connection to the host using default settings
## (ANONYMOUS authentication, etc.).
##
conn = Connection(HOST)
app  = Server(conn)

try:
    ##
    ## This server does nothing other than service requests asynchronously.
    ## Rather than idle the main thread, the Connection.run() call gives the
    ## main thread to the connection.  This application is therefore single-threaded.
    ##
    app.run()
except KeyboardInterrupt:
    pass

##
## Close the connection and everything associated with it.
##
conn.close()

