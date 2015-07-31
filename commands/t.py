from dckrmgr import commands

def func(cli, p_cwd, j_cnf):
    cli.stop(j_cnf['name'])
    print('Stopped ' + j_cnf['name'])
    return 0

commands['t'] = {
    'help': 'Stop container',
    'func': func
}
