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

from redpoll import Connection

class Custom(object):

    def __init__(self):
        self.addr = None
        self.conn = None

    def on_start(self, conn):
        """
        """
        self.conn = conn
        self.addr = self.conn.get_addr()

    def on_stop(self, conn):
        """
        """
        pass

    def on_connected(self, conn):
        """
        """
        pass

    def on_opened(self, conn):
        """
        """
        pass

    def on_closed(self, conn):
        """
        """

    def on_disconnected(self, conn, reason):
        """
        """
        pass

##
## Create, open, and maintain a connection to the group using ZooKeeper.
##
conn = Connection("discover:(fabric:us-east)", handler=ConnZookeeper())
conn.start()

##
## Normal messaging operations against the connection here.
##
pass

##
## Shut down the connection and everything associated with it.
##
conn.stop()

