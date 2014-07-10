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

class DynamicSource(object):
    """
    """

RECEIVER_AUTO_ACCEPT   = 1
RECEIVER_AT_LEAST_ONCE = 2
RECEIVER_EXACTLY_ONCE  = 3
DIST_MOVE              = 1  # consume
DIST_COPY              = 2  # browse
DYNAMIC                = DynamicSource()

class ReceiverHandler(object):
    """
    """

    def on_message(self, receiver, msg):
        """
        """
        pass

    def on_settle(self, receiver, msg):
        """
        """
        pass

    def on_close(self):
        """
        """
        pass

class Receiver(object):
    """
    """

    def __init__(self, conn_or_sess, source, target=None, handler=None, delivery_mode=RECEIVER_AUTO_ACCEPT, link_recovery=False, prefetch=0, selector=None, dist_mode=DIST_MOVE):
        """
        """
        pass

    def close(self):
        """
        """
        pass

    def recv(self, timeout=None):
        """
        """
        pass

    def accept(self, msg, transaction=None):
        """
        """
        pass

    def reject(self, msg, transaction=None):
        """
        """
        pass

    def settle(self, msg, transaction=None):
        """
        """
        pass

    def add_credit(self, credits=1):
        """
        """
        pass

    def get_source(self):
        """
        """
        pass
