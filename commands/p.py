from dckrmgr import cli
from dckrmgr import m_cmd

def func(ctx):
    cnf = ctx['cnf']
    image = cnf['image']['name'] + ':' + cnf['image']['version']
    # from https://docker-py.readthedocs.org/en/latest/api/
    for line in cli.pull(image, stream=True):
        print(json.dumps(json.loads(line), indent=4))
    return 0

m_cmd['p'] = {
    'hlp': 'Pull container',
    'ord': 'nrm',
    'fnc': func
}
