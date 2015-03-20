#!/usr/bin/env python

__author__ = 'arobres'
from fabric.api import env
import fabtools
import argparse
from configuration import computer_ips

env.user = 'fedora'
env.key_filename = '~/.ssh/sshkeyforinstances.pem'


def status_service(service_name):

    if fabtools.systemd.is_running(service_name):
        print("Service {} is running!".format(service_name))
    else:
        print("Service {} is not running!".format(service_name))


def start_service(service_name):

    fabtools.systemd.start(service_name)
    status_service(service_name)


def stop_service(service_name):

    fabtools.systemd.stop(service_name)
    status_service(service_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="Define the IP or hostname of the host to operate", default=None, required=False)
    parser.add_argument("--hostname", help="Define the name from configuration file", default=None, required=False)
    parser.add_argument("--service", help="Define the service to operate", default=None, required=True)
    parser.add_argument("--action", help="Define the operation to perform", default=None, choices=["status", "start",
                                                                                                       "stop"], required=True)
    args = parser.parse_args()

    if args.host is None and args.hostname is None:
        print "Host or Hostname are required arguments"
        exit(1)

    if args.host is not None and args.hostname is not None:
        print "Only one parameters (between host or hostname) is allowed"
        exit(1)

    if args.hostname is not None:
        env.host_string = computer_ips[args.hostname]
    else:
        env.host_string = args.host

    if args.action == 'status':
        status_service(args.service)
    elif args.action == 'start':
        start_service(args.service)
    elif args.action == 'stop':
        stop_service(args.service)

if __name__ == "__main__":
    main()