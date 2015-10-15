from dckrmgr import cli
from dckrmgr import m_cmd

import os
import docker

def func(ctx):
    cnf = ctx['cnf']
    p_cwd = ctx['p_cwd']

    environment = {}

    for variable in cnf.get('environment', {}):
        environment[variable['name']] = variable['value']

    volumes = []
    binds = {}

    for volume in cnf.get('volumes', {}):
        volumes.append(volume['container_path'])

        binds[os.path.join(p_cwd, volume['host_path'])] = {
            'bind': volume['container_path'],
            'mode': volume['mode']
        }

    ports = []
    port_bindings = {}

    for port in cnf.get('ports', {}):
        if 'protocol' in port and port['protocol'] == 'udp':
            p = (port['container_port'], 'udp')
            p_hc = str(port['container_port']) + '/udp'
        else:
            p = port['container_port']
            p_hc = port['container_port']

        if 'address' in port:
            h = (port['address'], port['host_port'])
        else:
            h = port['host_port']

        ports.append(p)
        port_bindings[p_hc] = h

    links = {}

    for link in cnf.get('links', {}):
        links[link['name']] = link['alias']

    host_config = cli.create_host_config(
        binds = binds,
        port_bindings = port_bindings,
        links = links
    )

    try:
        res = cli.create_container(
            name = cnf['name'],
            image = cnf['image']['name'] + ':' + cnf['image']['version'],
            hostname = cnf.get('hostname'),
            environment = environment,
            volumes = volumes,
            ports = ports,
            host_config = host_config
        )
    except docker.errors.APIError as detail:
        print('Couldn\'t create ' + cnf['name'] + ':')
        print(detail)
        return 1

    print('Created ' + cnf['name'])

    if res['Warnings'] != None:
        print('Warnings generated:')
        print(res['Warnings'])

    return 0

m_cmd['c'] = {
    'hlp': 'Create container',
    'ord': 'nrm',
    'fnc': func
}
