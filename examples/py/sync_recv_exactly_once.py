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

HOST = "localhost:5672"
DEST = "destination"

##
## Create and open a connection to the host using default settings
## (ANONYMOUS authentication, etc.).
##
conn = Connection(HOST)
conn.start()

##
## Create a receiver-link from the destination source on the connected container.
## A delivery mode of exactly-once is selected meaning that this receiver will
## use the 3-ack protocol and message de-duplication to deliver each message only
## once.
##
link = Receiver(conn, DEST, delivery_mode=RECEIVER_EXACTLY_ONCE)

##
## Receive a message, blocking until the message arrives.
##
msg = link.recv()
print msg.body

##
## Accept the message.  This causes the accept disposition to be sent, unsettled,
## back to the sender.
##
link.accept(msg)

##
## Close the connection and everything associated with it.
## This call will block until the 3-ack exchange is completed.  This call will not block
## longer than the default force_timeout.
##
conn.close()

