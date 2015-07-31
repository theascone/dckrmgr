from dckrmgr import commands

def func(cli, p_cwd, j_cnf):
    cli.start(j_cnf['name'])
    print('Started ' + j_cnf['name'])
    return 0

commands['s'] = {
    'help': 'Start container',
    'func': func
}
