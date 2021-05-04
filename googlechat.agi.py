"""
Fast AGI service to send messages to a Google Chat webhook (async)
"""

import json
import os
import socketserver
import sys
import threading
import time

import requests
import yaml
from asterisk.agi import AGI

config = {"webhook": os.environ.get("WEBHOOK"),
          "host": os.environ.get("HOST"),
          "port": os.environ.get("PORT"),
          "timeout": os.environ.get("TIMEOUT")}

if config["webhook"] is not None \
        and config["host"] is not None \
        and config["port"] is not None \
        and config["timeout"] is not None:

    print("Got configuration from environment", end=": ")
    print(config)

else:
    print("Loading config file config.yaml")
    try:
        with open("config.yaml", 'r') as stream:
            try:
                config = yaml.safe_load(stream)
                print("Got configuration from config.yaml", end=": ")
                print(config)
            except yaml.YAMLError as exc:
                print("Error opening config.yaml")
                print(exc)
    except FileNotFoundError:
        print("config.yaml not found and environment not set. Can't continue. Exiting.")
        sys.exit(-1)

if not config["webhook"] or not config["host"] or not config["port"] or not config["timeout"]:
    print(config)
    print("Missing config option(s). Exiting.")
    sys.exit(-1)


def post_message(content):
    """
    Method to post message to Google Chat
    :return:
    """
    content = {
        "text": content
    }
    requests.request(url=config["webhook"], data=json.dumps(content), method="POST", headers={
        "Content-Type": "application/json; charset=UTF-8"
    })


class FastAGI(socketserver.StreamRequestHandler):
    """
    FastAGI request handler for socketserver
    """
    timeout = int(config["timeout"])

    def handle(self):
        try:
            agi = AGI(stdin=self.rfile, stdout=self.wfile, stderr=sys.stderr)
            senderthread = threading.Thread(target=post_message, args=(agi.env["agi_arg_1"],))
            senderthread.start()
            time.sleep(.3)  # This is needed

        except TypeError as exception:
            sys.stderr.write('Unable to connect to agi://{} {}\n'.
                             format(self.client_address[0], str(exception)))
        except socketserver.socket.timeout as exception:
            sys.stderr.write('Timeout receiving data from {}\n'.
                             format(self.client_address))
        except socketserver.socket.error as exception:
            sys.stderr.write('Could not open the socket. '
                             'Is someting else listening on this port?\n')
        except Exception as exception:  # pylint: disable=broad-except
            sys.stderr.write('An unknown error: {}\n'.
                             format(str(exception)))


if __name__ == "__main__":
    # Create socketServer
    server = socketserver.ForkingTCPServer((config["host"], int(config["port"])), FastAGI)
    print("Starting FastAGI server on " + config["host"] + ":" + str(config["port"]))

    # Keep server running until CTRL-C is pressed.
    server.serve_forever()
