## Redpoll Tutorial: Sending and Receiving Messages

### Simple Message Send

To send messages, you must first create a Sender.

    sender = Sender(connection, "my-queue")

As you can see, the sender is created in the context of a connection and an
address is supplied as the sender's target.  For this example, the address
"my-queue" names a queue that exists on the connected message broker.
Addresses can be used for other purposes as well, but we'll talk about that in
a different section.

The next thing you need in order to send a message is to create a message with
the content you wish to send.  This is done by creating a Message object.

    message = Message("Message Content")

This example shows the creation of a message that contains a text string.
AMQP messages may also carry other types of content, like an integer:

    message = Message(365)

or a composite type:

    content = {'first_name' : 'Joseph', 'last_name' : 'Sixpack', 'age' : 34}
    message = Message(content)

The message is then sent via the Sender:

    sender.send(message)

Putting it all together, we can write a simple program to send a message to a
queue on a message broker:

    from redpoll import Connection, Sender, Message
    connection = Connection("localhost")
    connection.start()

    sender = Sender(connection, "my-queue")
    sender.send(Message("Message Content"))

    connection.stop()

So what's really going on in this example?

 - We've created a connection to a broker running on the same host.  This
   broker doesn't require authentication (it accepts ANONYMOUS connections).
 - We started the connection, allowing Redpoll to create a thread to manage
   the connection for us.
 - We created a sender to "my-queue", a node on the the broker to which we
   want to send messages.  No additional options are provided for the sender,
   so it uses the default settings.  The important default is the
   delivery_mode of _SENDER_PRESETTLED_.  This causes the messages sent
   through this sender to be _pre-settled_, or _best-effort_, sometimes also
   referred to as _fire-and-forget_.  It really means that the sender does not
   expect the receiver to acknowledge the receipt of any of the messages.  The
   receiver will be told this and will not attempt to acknowledge any of the
   received messages.
 - We then use send() to send a message through the sender.  Again, we have
   provided no additional options so send defaults to a synchronous
   operation.  Since we are using pre-settled message delivery, send does not
   block unless there is flow-control back-pressure from the receiver.  If the
   receiver has not issued any flow-control credit, send will block until
   there is enough credit to send one message.
 - Stopping the connection ensures that all in-flight operations are complete,
   closes the connection cleanly, then terminates the thread that was managing
   the connection.

<hr width="80%"/>
 - [Up: Table of Contents](toc.md)
 - [Next: Simple Message Receive](recv-simple.md)
