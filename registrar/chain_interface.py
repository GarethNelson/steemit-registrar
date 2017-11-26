import requests
import uuid

import steem
import steembase
from steem.blockchain import Blockchain
from steem.commit import Commit
from steem.wallet import Wallet
import pprint
import json
import logging
logger = logging.getLogger(__name__)

class ChainInterface:
   chain_id     = '0000000000000000000000000000000000000000000000000000000000000000'
   chain_prefix = 'STM'
   steem_symbol = 'STEEM'
   sbd_symbol   = 'SBD'
   vests_symbol = 'VESTS'
   steemd_nodes = ['https://api.steemit.com','https://steemd.steemit.com']

   def __init__(self,debug_mode=False):
       self.steemd_rpc = steem.steemd.Steemd(nodes=self.steemd_nodes)
       self.debug_mode = debug_mode
       steembase.chains.known_chains['STEEM'] = {
        'chain_id'    :self.chain_id,
        'prefix'      :self.chain_prefix,
        'steem_symbol':self.steem_symbol,
        'sbd_symbol'  :self.sbd_symbol,
        'vests_symbol':self.vests_symbol
       }

   def use_botuser(self,botuser=None):
       """ Tell the interface what the username/password for bot user is
       """
       self.bot_username = botuser.username
       self.bot_password = botuser.password

       self.keys = [str(botuser.posting_key.get_private_key()),
                    str(botuser.active_key.get_private_key()),
                    str(botuser.owner_key.get_private_key())]
       pprint.pprint(self.keys)
       self.wallet = Wallet(steemd_instance = self.steemd_rpc, keys=[])
       self.wallet.prefix = self.chain_prefix
       self.wallet.setKeys(self.keys)

   def get_steem_committer(self):
       retval = Commit(steemd_instance = self.steemd_rpc,
                       debug=self.debug_mode,
                       keys=self.keys)
       return retval

   def register_user(self,new_username=None,new_password=None):
       """ Attempt to register a new user on the blockchain
       """
       committer = self.get_steem_committer()
       retval = committer.create_account(new_username,password=new_password,store_keys=False,creator=self.bot_username)
       return retval

class TestnetInterface(ChainInterface):
   chain_id     = '79276aea5d4877d9a25892eaa01b0adf019d3e5cb12a97478df3298ccdd01673'
   chain_prefix = 'STM'
   steemd_nodes = ['https://testnet.steem.vc']

   def create_bot_user(self,username,password):
       r = requests.post('https://testnet.steem.vc/create',data={'username':username,'password':password})
       pprint.pprint(r.text)
       if r.status_code == 200:
          return
       raise Exception()

class SteemitBotUser:
   """ Represents a user used by the registrar
   """
   def __init__(self,chain=None,username=None,password=None):
       """ If username+password are None, this will attempt to create a user, if the underlying chain interface supports it.
           This means it only really works for Testnet.
           If chain is None, this defaults to Testnet
       """
       if chain is None: chain = TestnetInterface()
       self.chain = chain

       if (username is None) or (password is None):
          if username is None: self.username = 'botuser%s' % str(uuid.uuid4())[:8]
          if password is None: self.password = str(uuid.uuid4())
          self.chain.create_bot_user(self.username,self.password)
       else:
         self.username = username
         self.password = password
       self.posting_key = steembase.account.PasswordKey(self.username, self.password, role="posting")
       self.active_key  = steembase.account.PasswordKey(self.username, self.password, role="active")
       self.owner_key  = steembase.account.PasswordKey(self.username, self.password, role="owner")


