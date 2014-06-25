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

    def on_open(self):
        """
        """
        pass

    def on_close(self, reason):
        """
        """
        pass


class Connection(object):
    """
    """

    def __init__(self, hostport_or_transport, handler=None):
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

    def set_host(self, host_port):
        """
        """
        pass

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


    ##===========================================================================
    ## Transport extension interface
    ##===========================================================================

    def xport_read_ready(self):
        """
        """
        pass

    def xport_write_ready(self):
        """
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

