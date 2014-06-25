Python Examples
===============

# Synchronous Examples

<center>
<table>
  <tr><th>Example File</th><th>Description</th></tr>
  || sync_send_presettled.py || Simplest possible message sender ||
  || sync_recv_autoaccepted.py || Simplest possible message receiver ||
  || sync_send_reliable.py || Sending messages that need to be acknowledged ||
  || sync_recv_exactly_once.py || Receiver of messages using the exactly-once mode ||
  || sync_client_best_effort.py || The client-side of a simple best-effort request-response application ||
  || sync_server_best_effort.py || The server-size of a simple best-effort request-response application ||
</table>
</center>

# Asynchronous Examples

# Needed Additions

 - TCP Server, using an FD transport extension (internal thread via connection.start())
 - Running with an external select loop (external thread pool)
 - Doing transactional work
 - Connecting with SSL and SASL
 - Link recovery
