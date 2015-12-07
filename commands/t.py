from dckrmgr import cli
from dckrmgr import m_cmd
import requests

def func(ctx):
    cnf = ctx['cnf']
    try:
      cli.stop(cnf['name'])
      print('Stopped ' + cnf['name'])
    except requests.exceptions.HTTPError:
      print('Could not stop ' + cnf['name'] + '!')
    return 0

m_cmd['t'] = {
    'hlp': 'Stop container',
    'ord': 'rev',
    'fnc': func
}
