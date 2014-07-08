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

HOST  = "localhost:5672"
DEST  = "destination"
COUNT = 100

class Example(object):
    def __init__(self, host):
        self.conn          = Connection(host)
        self.link          = Sender(self.conn, DEST, handler=self, delivery_mode=SENDER_REQUIRE_ACK)
        self.settled_count = 0

    def on_settle(self, link, msg, disposition, reason):
        """
        Stop the application once all of the messages are sent and acknowledged,
        """
        self.settled_count += 1
        if self.settled_count == COUNT:
            self.conn.stop()

    def run(self):
        self.conn.start()
        for i in range(COUNT):
            msg= Message({'sequence':i})
            sender.send(msg, handler=self)
        self.conn.wait()

app = Example(HOST)
app.run()

