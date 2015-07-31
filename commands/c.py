from dckrmgr import commands

import os
import docker

def func(cli, p_cwd, j_cnf):
    environment = {}

    for variable in j_cnf.get('environment', {}):
        environment[variable['name']] = variable['value']

    volumes = []
    binds = {}

    for volume in j_cnf.get('volumes', {}):
        volumes.append(volume['container_path'])

        binds[os.path.join(p_cwd, volume['host_path'])] = {
            'bind': volume['container_path'],
            'mode': volume['mode']
        }

    ports = []
    port_bindings = {}

    for port in j_cnf.get('ports', {}):
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

    for link in j_cnf.get('links', {}):
        links[link['name']] = link['alias']

    host_config = docker.utils.create_host_config(
        binds = binds,
        port_bindings = port_bindings,
        links = links
    )

    try:
        res = cli.create_container(
            name = j_cnf['name'],
            image = j_cnf['image']['name'] + ':' + j_cnf['image']['version'],
            hostname = j_cnf.get('hostname'),
            environment = environment,
            volumes = volumes,
            ports = ports,
            host_config = host_config
        )
    except docker.errors.APIError as detail:
        print('Couldn\'t create ' + j_cnf['name'] + ':')
        print(detail)
        return 1

    print('Created ' + j_cnf['name'])

    if res['Warnings'] != None:
        print('Warnings generated:')
        print(res['Warnings'])

    return 0

commands['c'] = {
    'help': 'Create container',
    'func': func
}
