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

from proton.handlers import MessagingHandler
from proton.reactor import EventInjector, ApplicationEvent

class LockException(Exception):
    pass


class Lock(MessagingHandler):
    def __init__(self, reactor, connection, lock_name, label=None, user_context=None):
        super(Lock, self).__init__(prefetch=0, auto_accept=False, auto_settle=False)
        self.reactor        = reactor
        self.connection     = connection
        self.lock_name      = lock_name
        self.user_context   = user_context
        self.acquired_state = False
        self.events         = EventInjector()
        self.reactor.selectable(self.events)

        self.lock_receiver = None

    def destroy(self):
        if self.acquired_state and self.lock_receiver:
            self.lock_receiver.close()
        self.events.close()

    @property
    def is_acquired(self):
        return self.acquired_state

    def acquire(self):
        if self.acquired_state:
            raise LockException("Lock already acquired")
        self.lock_receiver = self.reactor.create_receiver(self.connection, self.lock_name, handler=self)

    def release(self):
        if not self.acquired_state:
            raise LockException("Lock not acquired")
        self.acquired_state = False
        self.lock_receiver.close()

    def on_link_opened(self, event):
        if event.receiver == self.lock_receiver and event.receiver.remote_source.address == self.lock_name:
            self.acquired_state = True
            new_event = ApplicationEvent("lock_acquired")
            new_event.user_context = self.user_context
            self.events.trigger(new_event)

    def on_link_error(self, event):
        if event.receiver == self.lock_receiver:
            new_event = ApplicationEvent("lock_failed")
            new_event.user_context = self.user_context
            new_event.error        = event.link.remote_condition
            self.events.trigger(new_event)

    def on_link_closed(self, event):
        if event.receiver == self.lock_receiver and self.acquired_state:
            self.acquired_state = False
            new_event = ApplicationEvent("lock_released")
            new_event.user_context = self.user_context
            self.events.trigger(new_event)
