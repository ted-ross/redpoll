## Redpoll Tutorial: Sending and Receiving Messages

### Simple Message Receive

To receive messages, you must first create a Receiver.

    receiver = Receiver(connection, "my-queue")

Like the sender, a receiver is created in the context of a connection and
contains an address to identify the receiver's source (in this case, the same
queue on the same broker).

To receive a message through the receiver, we use the recv() function:

    message = receiver.recv()

Putting it all together, we can write a simple program to receive a message
from a queue on a message broker:

    from redpoll import Connection, Receiver
    connection = Connection("localhost")
    connection.start()

    receiver = Receiver(connection, "my-queue")
    message = receiver.recv()
    print message.body

    connection.stop()

So what's really going on in this example?

 - We've created a connection to a broker running on the same host.  This
   broker doesn't require authentication (it accepts ANONYMOUS connections).
 - We started the connection, allowing Redpoll to create a thread to manage
   the connection for us.
 - A receiver is created for the connection for source address "my-queue".
   This causes Redpoll to create an AMQP session and an incoming link in that
   session with a source address of "my-queue".  No additional options are
   selected so the default options take effect:
   - deliver_mode = _RECEIVER_AUTO_ACCEPT_ - This causes the receiver to
     automatically accept and settle any incoming deliveries that are not
     pre-settled by the sender.  This applies only to messages that are passed
     to the application via the recv() function.
   - prefetch = _0_ - The receiver will not issue any credit by default.
     Credit is issued when the recv() call is invoked.
   - dist_mode = _DIST_MOVE_ - The receiver will consume (move) the received
     messages as opposed to browsing (copy) them.
 - receiver.recv() is a synchronous function that will block until there is a
   message to receive.  Recv pre-issues a replacement credit for the message
   it will receive.  This prevents deadlocking on a link with no issued
   credit.
 - The .body member of the received message is the content with which the
   message was created by the sender.
 - The connection is stopped, cleanly closing the link, session, and
   connection before terminating the connection's worker thread.

<hr width="80%"/>
 - [Up: Table of Contents](toc.md)
 - [Prev: Simple Message Send](send-simple.md)
 - [Next: ???](.md)
