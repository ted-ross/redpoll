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

from redpoll import Connection, Receiver, RECEIVER_EXACTLY_ONCE
from time import sleep

HOST  = "localhost:5672"
DEST  = "destination"

class Example(object):
    def __init__(self, conn):
        self.conn = conn
        self.link = Receiver(self.conn, DEST, handler=self, delivery_mode=RECEIVER_EXACTLY_ONCE)

    def on_message(self, link, msg):
        print msg.body
        link.accept(msg)

##
## Create a connection to the host using default settings
## (ANONYMOUS authentication, etc.).
##
conn = Connection(HOST)

##
## Start the connection.  This causes a thread to be created by the library
## to handle messaging operations and to invoke callbacks.
##
conn.start()

app = Example(conn)

##
## While app asynchronously receives and accepts messages, the main application
## can proceed with other work.
##
try:
    while True:
        sleep(1.0)
except KeyboardInterrupt:
    pass

##
## Close the connection and everything associated with it.
##
conn.stop()

