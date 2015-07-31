from dckrmgr import commands

def func(cli, p_cwd, j_cnf):
    cli.remove_container(container = j_cnf['name'])
    print('Removed ' + j_cnf['name'])
    return 0

commands['r'] = {
    'help': 'Remove container',
    'func': func
}
