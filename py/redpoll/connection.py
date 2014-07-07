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


class ConnectionHandler(object):
    """
    """

    def on_start(self, conn):
        """
        """
        pass

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


class Connection(object):
    """
    """

    def __init__(self, addr_or_transport, handler=None):
        """
        """
        pass

    def start(self):
        """
        """
        pass

    def run(self):
        """
        """
        pass

    def stop(self, force_timeout=10):
        """
        """
        pass

    def reconnect(self):
        """
        """
        pass

    def set_addr(self, addr):
        """
        """
        pass

    def get_addr(self):
        """
        """
        return None

    def set_sasl(self, mechanisms):
        """
        """
        pass

    def set_ssl(self, cert_file, pvt_key_file, password, trusted_cert_db, trusted_certs, peer_auth):
        """
        """
        pass

    def set_annotations(self, annotation_map):
        """
        """
        pass

    def set_max_frame_size(self, max_frame):
        """
        """
        pass

    def set_heartbeat(self, interval, loss_tolerance):
        """
        """
        pass

    def get_remote_container_info(self):
        """
        """
        pass

    def get_sasl_info(self):
        """
        """
        pass

    def get_ssl_info(self):
        """
        """
        pass


    ##===========================================================================
    ## Transport extension interface
    ##===========================================================================

    def xport_pre_poll(self):
        """
        Invoked by the transport prior to blocking in poll/select.
        The connection may use this call to do internal processing.

        The connection returns a three-tuple:  (read_ready, write_ready, timeout)

        read_ready and write_ready are boolean values indicating whether the connection
        wishes to read and write respectively.

        timeout is a duration in milliseconds for when the connection wishes to be
        pre_polled again.  The poll loop should use the minimum of the timeouts for
        all connections it is managing.
        """
        pass

    def xport_read(self, xport):
        """
        """
        pass

    def xport_write(self, xport):
        """
        """
        pass

    def xport_timeout(self):
        """
        """
        pass


    ##===========================================================================
    ## SASL extension interface
    ##===========================================================================

