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

from redpoll import Connection, Sender, Message, SENDER_REQUIRE_ACK
from redpoll.extensions import AmqpLocalTransaction

HOST = "localhost:5672"
DEST = "queue"

##
## Create and open a connection to the host using default settings
## (ANONYMOUS authentication, etc.).
##
conn = Connection(HOST)
conn.start()

##
## Create a sender-link to the destination target on the connected container.
## Set the delivery mode to require-ack, meaning that synchronous sends will
## block until the message delivery is settled.
##
link = Sender(conn, DEST, delivery_mode=SENDER_REQUIRE_ACK)

##
## Create an instance of an AMQP local transaction
##
txn = AmqpLocalTransaction(conn)

##
## Send the messages, blocking until the delivery is settled.
## Each send is delivered in the context of the transaction.
##
for i in range(5):
    msg = Message(i)
    disposition = link.send(msg, transaction=txn)
msg = Message()
msg.application_headers['end'] = None
link.send(msg, transaction=txn)

##
## Commit the transaction so the effect of the sent deliveries can be
## seen outside the transaction.  Alternatively, txn.rollback() could be called
## to make it as though the deliveries never happened.
##
txn.commit()

##
## Close the connection and everything associated with it.
##
conn.stop()

