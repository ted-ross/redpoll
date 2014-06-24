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

from qpid.messaging import Connection, Sender, Message

HOST = "localhost:5672"
DEST = "destination"
BODY = {'first':445, 'second':'string value'}

##
## Create and open a connection to the host using default settings
## (ANONYMOUS authentication, etc.).
##
conn = Connection(HOST)
conn.open()

##
## Create a sender-link to the destination target on the connected container.
##
link = Sender(conn, DEST)

##
## Create a message with some content.
##
msg = Message(BODY)

##
## Send the message pre-settled, blocking until the message leaves the process.
##
link.send(msg)

##
## Close the connection and everything associated with it.
##
conn.close()
