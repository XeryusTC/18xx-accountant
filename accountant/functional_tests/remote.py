# -*- coding: utf-8 -*-
from collections import namedtuple

from ansible import constants as C
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts',
    'syntax', 'connection', 'module_path', 'forks', 'remote_user',
    'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
    'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity',
    'check'])

def run_playbook(playbook_file, inventory_file):
    variable_manager = VariableManager()
    loader = DataLoader()
    options = Options(listtags=False, listtasks=False, listhosts=False,
        syntax=False, connection=C.DEFAULT_TRANSPORT, module_path=None,
        forks=100, remote_user=None, private_key_file=None,
        ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None,
        scp_extra_args=None, become=False, become_method=None,
        become_user=None, verbosity=C.DEFAULT_VERBOSITY, check=False)

    # Load the inventory file
    inventory = Inventory(loader=loader, variable_manager=variable_manager,
        host_list=inventory_file)
    variable_manager.set_inventory(inventory)

    pbex = PlaybookExecutor(playbooks=[playbook_file], inventory=inventory,
        variable_manager=variable_manager, loader=loader, options=options,
        passwords=None)
    pbex.run()
