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

RECEIVER_AUTO_ACCEPT   = 1
RECEIVER_AT_LEAST_ONCE = 2
RECEIVER_EXACTLY_ONCE  = 3
DIST_MOVE              = 1  # consume
DIST_COPY              = 2  # browse


class ReceiverHandler(object):
    """
    """

    def onMessage(self, receiver, msg):
        """
        """
        pass

    def onSettle(self, receiver, msg):
        """
        """
        pass

    def onClose(self):
        """
        """
        pass


class Receiver(object):
    """
    """

    def __init__(self, conn_or_sess, source, target=None, delivery_mode=RECEIVER_AUTO_ACCEPT, link_recovery=False, initial_credit=10, selector=None, dist_mode=DIST_MOVE):
        """
        """
        pass

    def close(self):
        """
        """
        pass

    def recv(self):
        """
        """
        pass

    def accept(self, msg):
        """
        """
        pass

    def reject(self, msg):
        """
        """
        pass

    def release(self, msg):
        """
        """
        pass

    def settle(self, msg):
        """
        """
        pass

    def add_credit(self, credits=1):
        """
        """
        pass
