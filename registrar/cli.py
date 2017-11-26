import argparse
import os
import sys

import uuid
import pprint

import logging
import json

logger = logging.getLogger(__name__)


from .chain_interface import ChainInterface
from .chain_interface import TestnetInterface
from .chain_interface import SteemitBotUser

def main():
    parser = argparse.ArgumentParser(description="Steemit registration server")
    parser.add_argument('-d','--dev',        action='store_true', help='Start in development/debug mode')
    parser.add_argument('-t','--testnet',    action='store_true', help='Use testnet instead of main blockchain')
    parser.add_argument('-l','--listen_port',type=int,            help='Port to listen on for HTTP server',default=8090)
    parser.add_argument('-u','--username',   type=str,            help='Username to use for the bot user',default=None)
    parser.add_argument('-p','--password',   type=str,            help='Password to use for the bot user',default=None)
    args = parser.parse_args(sys.argv[1:])

    if args.dev:
       logging.basicConfig(level='DEBUG')
       debug_mode = True
    else:
       logging.basicConfig(level='INFO')
       debug_mode = False

    if args.testnet:
       chain    = TestnetInterface(debug_mode=debug_mode)
    else:
       chain = MainchainInterface(debug_mode=debug_mode)

    botuser = SteemitBotUser(chain=chain,username=args.username,password=args.password)
    chain.use_botuser(botuser=botuser)

    if debug_mode:
       new_username = 'debug%s' % str(uuid.uuid4())[:8]
       new_password = str(uuid.uuid4())
       print(chain.register_user(new_username,new_password).toJson())
     

if __name__ == '__main__':
    main()
