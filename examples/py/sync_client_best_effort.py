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

from qpid.messaging import Connection, Sender, Receiver, Message, DYNAMIC

HOST = "localhost:5672"
DEST = "destination"
BODY = {'op':'echo', 'data':'string value'}

##
## Create and open a connection to the host using default settings
## (ANONYMOUS authentication, etc.).
##
conn = Connection(HOST)
conn.start()

##
## Create a sender-link to the destination target on the connected container.
##
request_link = Sender(conn, DEST)

##
## Create a receiver link for the response.  Use the DYNAMIC source so the
## system can assign a useful reply-to address for the response.
##
response_link = Receiver(conn, DYNAMIC)
reply_to = response_link.get_source()

##
## Create a request message with some content and set the reply-to header.
##
request = Message(BODY)
request.reply_to = reply_to

##
## Send the message pre-settled, blocking until the message leaves the process.
##
request_link.send(request)

##
## Block waiting for the response message on the response link.
##
response = response_link.recv()
print response.body

##
## Close the connection and everything associated with it.
##
conn.close()

