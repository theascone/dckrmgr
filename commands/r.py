from dckrmgr import cli
from dckrmgr import m_cmd
import requests

def func(ctx):
    cnf = ctx['cnf']
    try:
      cli.remove_container(container = cnf['name'])
      print('Removed ' + cnf['name'])
    except requests.exceptions.HTTPError:
      print('Could not remove ' + cnf['name'] + '!')

    return 0

m_cmd['r'] = {
    'hlp': 'Remove container',
    'ord': 'rev',
    'fnc': func
}
