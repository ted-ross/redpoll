redpoll
=======

Simple Managed Connectivity for Cloud Applications

## Project Status

The redpoll project is a work in development.  All libraries in this
project are experimental in nature and should not be considered
stable until officially released.

## Introduction

Redpoll provides a set of libraries and services that run on an AMQP
(Advanced Message Queuing Protocol) network.  The components of this
project are built on top of AMQP client libraries available from
Apache Qpid Proton and Rhea.

The goal of Redpoll is to make it easy to develop and operate
distributed applications that run in hybrid cloud and multi-site
environments.

Redpoll is about the interconnection of distributed components.  It
supports a variety of useful communication patterns and provides
services to both help coordinate distributed workloads and to manage
and monitor those workloads in an operational environment.

## AMQP Networking

The AMQP protocol has a number of characteristics that make it ideal
for interconnect in hybrid cloud and multi-site situations.

AMQP has rich addressing and multiplexing capabilities that make ita
routable protocol.  AMQP routing occurs at layer seven, independently
of the layer three routing that is provided by IP.  This provides a
number of significant benefits for developers and operators of
distributed systems:

- AMQP routing overlays the IP network, permitting data senders and
  receivers, or clients and servers to be located anywhere in an IP
  network.  This means that servers can be located in private IP
  networks yet accessible from cloud data centers or other private
  networks.  This connectivity does not require the deployment of
  tunnels or VPNs.
- Load balancing is built into the network without the need for
  deploying load balancers.  Furthermore, load balancing takes
  advantage of the protocol's knowledge of the disposition of data
  delivery.  This means that load can be balanced based on a
  receiver's or server's actual rate of processing in real time rather
  than using round-robin or some out-of-band load measuring
  mechanism.
- Security and access policy can be applied at the application layer,
  in terms of actual services, users, and processes.  There is no need
  to try to express business policy in terms of layer-four network
  concepts employed by firewalls.

## Communication Patterns

### Direct Request Response
