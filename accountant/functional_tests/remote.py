# -*- coding: utf-8 -*-
from collections import namedtuple

from ansible import constants as C
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.utils.vars import load_extra_vars
from ansible.plugins.callback import CallbackBase

Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts',
    'syntax', 'connection', 'module_path', 'forks', 'remote_user',
    'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
    'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity',
    'check', 'extra_vars'])

class ResultCallback(CallbackBase):
    def __init__(self):
        super(ResultCallback, self).__init__()
        self.results = []

    def v2_runner_on_ok(self, result, **kwargs):
        self.results.append(result)


def run_playbook(playbook_file, inventory_file, extra_vars=None):
    if extra_vars is None:
        extra_vars = {}

    variable_manager = VariableManager()
    loader = DataLoader()
    options = Options(listtags=False, listtasks=False, listhosts=False,
        syntax=False, connection=C.DEFAULT_TRANSPORT, module_path=None,
        forks=100, remote_user=None, private_key_file=None,
        ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None,
        scp_extra_args=None, become=False, become_method=None,
        become_user=None, verbosity=C.DEFAULT_VERBOSITY, check=False,
        extra_vars=extra_vars)

    # Load the extra vars
    variable_manager.extra_vars = extra_vars
    # Load the inventory file
    inventory = Inventory(loader=loader, variable_manager=variable_manager,
        host_list=inventory_file)
    variable_manager.set_inventory(inventory)

    pbex = PlaybookExecutor(playbooks=[playbook_file], inventory=inventory,
        variable_manager=variable_manager, loader=loader, options=options,
        passwords=None)

    # Register a callback so that we can inspect the results
    callback = ResultCallback()
    pbex._tqm._callback_plugins.append(callback)

    # Run the playbook
    code = pbex.run()
    # User is most likely interested in output of last command, so get that
    out = callback.results[-1]._result['out']
    return code, out.strip(), callback.results

def flushdb(playbook_dir, inventory_file):
    playbook = playbook_dir.child('flushdb.yml')
    return run_playbook(playbook, inventory_file)

def creategame(playbook_dir, inventory_file, cash=12000):
    playbook = playbook_dir.child('creategame.yml')
    return run_playbook(playbook, inventory_file, extra_vars={'cash': cash})

def createplayer(playbook_dir, inventory, game, name, cash=0):
    playbook = playbook_dir.child('createplayer.yml')
    return run_playbook(playbook, inventory, extra_vars={
            'game': game,
            'player_name': name,
            'cash': cash,
        })

def createcompany(playbook_dir, inventory, game, name, cash=0, share_count=10,
        ipo_shares=10, bank_shares=0, text_color='black',
        background_color='white'):
    playbook = playbook_dir.child('createcompany.yml')
    return run_playbook(playbook, inventory, extra_vars={
            'game': game,
            'company_name': name,
            'cash': cash,
            'share_count': share_count,
            'ipo_shares': ipo_shares,
            'bank_shares': bank_shares,
            'text_color': text_color,
            'background_color': background_color,
        })
