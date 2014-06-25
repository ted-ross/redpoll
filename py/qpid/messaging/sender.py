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


SENDER_PRESETTLED  = 1
SENDER_REQUIRE_ACK = 2


class SendHandler(object):
    """
    """

    def on_accept(self, receiver, msg):
        """
        """
        pass

    def on_reject(self, receiver, msg, reason):
        """
        """
        pass

    def on_release(self, receiver, msg):
        """
        """
        pass

    def on_settle(self, receiver, msg):
        """
        """
        pass


class Sender(object):
    """
    """

    def __init__(self, conn_or_sess, target=None, source=None, delivery_mode=SENDER_PRESETTLED, link_recovery=False, compression=None):
        """
        """
        pass

    def close(self):
        """
        """
        pass

    def send(self, msg, handler=None, transaction=None, timeout=None):
        """
        """
        pass

    def drained(self):
        """
        """
        pass
