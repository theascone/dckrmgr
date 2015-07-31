from dckrmgr import cli
from dckrmgr import m_cmd

def func(ctx):
    cnf = ctx['cnf']
    cli.start(cnf['name'])
    print('Started ' + cnf['name'])
    return 0

m_cmd['s'] = {
    'hlp': 'Start container',
    'ord': 'nrm',
    'fnc': func
}
