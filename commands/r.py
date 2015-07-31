from dckrmgr import cli
from dckrmgr import m_cmd

def func(ctx):
    cnf = ctx['cnf']
    cli.remove_container(container = cnf['name'])
    print('Removed ' + cnf['name'])
    return 0

m_cmd['r'] = {
    'hlp': 'Remove container',
    'ord': 'rev',
    'fnc': func
}
