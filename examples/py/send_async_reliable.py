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

from qpid.messaging import Connection, Sender, Message, SENDER_REQUIRE_ACK
from threading import Condition

HOST = "localhost:5672"
DEST = "destination"


class Example(object):
    def __init__(self, conn):
        self.conn         = conn
        self.link         = Sender(self.conn, DEST, delivery_mode=SENDER_REQUIRE_ACK)
        self.cv           = Condition()
        self.accept_count = 0
        self.reject_count = 0
        self.outstanding  = 0

    def _check_done(self):
        self.cv.acquire()
        self.outstanding -= 1
        if self.outstanding == 0:
            self.cv.notify()
        self.cv.release()

    def on_accept(self, link, msg):
        self.accept_count += 1
        self._check_done()

    def on_reject(self, link, msg):
        self.reject_count += 1
        self._check_done()

    def run(self):
        self.outstanding = 100
        for i in range(100):
            msg = Message({'sequence':i})
            self.link.send(msg, handler=self)

        self.cv.acquire()
        while self.outstanding > 0:
            self.cv.wait()
        self.cv.release()

        print "Complete: %d accepted, %d rejected" % (self.accept_count, self.reject_count)


##
## Create a connection to the host using default settings
## (ANONYMOUS authentication, etc.).
##
conn = Connection(HOST)
conn.start()

app = Example(conn)
app.run()

##
## Close the connection and everything associated with it.
##
conn.close()

