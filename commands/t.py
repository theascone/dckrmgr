from dckrmgr import cli
from dckrmgr import m_cmd

def func(ctx):
    cnf = ctx['cnf']
    cli.stop(cnf['name'])
    print('Stopped ' + cnf['name'])
    return 0

m_cmd['t'] = {
    'hlp': 'Stop container',
    'ord': 'rev',
    'fnc': func
}
