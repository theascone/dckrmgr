import os
import sys
import json
import docker
import argparse
import jsonschema

class DckrMgr(object):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', dest='commands', action='append_const', const='c', help='Create container')
        parser.add_argument('-s', dest='commands', action='append_const', const='s', help='Start container')
        parser.add_argument('-t', dest='commands', action='append_const', const='t', help='Stop container')
        parser.add_argument('-r', dest='commands', action='append_const', const='r', help='Remove container')
        parser.add_argument('-p', dest='commands', action='append_const', const='p', help='Pull container')
        parser.add_argument('-b', dest='commands', action='append_const', const='b', help='Backup volumes')
        args = parser.parse_args()

        self.cli = docker.Client('unix://var/run/docker.sock')

        self.p_src = os.path.dirname(os.path.abspath(__file__))

        self.p_cwd = os.getcwd()
        self.p_cnf = os.path.join(self.p_cwd, 'dckrcnf.json')
        self.p_cch = os.path.join(self.p_cwd, 'dckrcch.json')

        try:
            f_cnf = open(self.p_cnf, 'r')
        except OSError:
            print('Couldn\'t open dckrcnf.json')
            exit(1)

        try:
            f_sch = open(os.path.join(self.p_src, 'dckrcnf.schema.json'), 'r')
        except OSError:
            print('Couldn\'t open dckrcnf.schema.json')
            exit(1)

        try:
            self.j_cnf = json.load(f_cnf)
        except ValueError:
            print('dckrcnf.json is invalid json')
            exit(1)

        try:
            j_sch = json.load(f_sch)
        except ValueError:
            print('dckrcnf.schema.json is invalid json')
            exit(1)

        try:
            jsonschema.validate(self.j_cnf, j_sch)
        except jsonschema.exceptions.ValidationError as detail:
            print(detail.message)
            exit(1)

        try:
            f_cch = open(self.p_cch, 'x')
        except OSError:
            pass
        else:
            json.dump({}, f_cch, indent = 4, sort_keys = True)

        try:
            f_cch = open(self.p_cch, 'r')
        except OSError:
            exit(1)

        self.j_cch = json.load(f_cch)

        i_sts = 0

        for command in args.commands:
            if getattr(self, command)() != 0:
                i_sts = 1
                break

        try:
            f_cch = open(self.p_cch, 'w')
        except OSError:
            exit(1)

        json.dump(self.j_cch, f_cch, indent = 4, sort_keys = True)

        exit(i_sts)

    def c(self):
        if 'id' in self.j_cch:
            print(self.j_cnf['name'] + ' already created')
            return 1

        environment = {}

        for variable in self.j_cnf['environment']:
            environment[variable['name']] = variable['value']

        volumes = []
        binds = {}

        for volume in self.j_cnf['volumes']:
            volumes.append(volume['container_path'])

            binds[os.path.join(self.p_cwd, volume['host_path'])] = {
                'bind': volume['container_path'],
                'mode': volume['mode']
            }

        ports = []
        port_bindings = {}

        for port in self.j_cnf['ports']:
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

        for link in self.j_cnf['links']:
            links[link['name']] = link['alias']

        host_config = docker.utils.create_host_config(
            binds = binds,
            port_bindings = port_bindings,
            links = links
        )

        try:
            res = self.cli.create_container(
                name = self.j_cnf['name'],
                image = self.j_cnf['image']['name'] + ':' + self.j_cnf['image']['version'],
                hostname = self.j_cnf.get('hostname'),
                environment = environment,
                volumes = volumes,
                ports = ports,
                host_config = host_config
            )
        except docker.errors.APIError as detail:
            print('Couldn\'t create ' + self.j_cnf['name'] + ':')
            print(detail)
            return 1

        self.j_cch['id'] = res['Id']

        print('Created ' + self.j_cnf['name'])

        if res['Warnings'] != None:
            print('Warnings generated:')
            print(res['Warnings'])

        return 0

    def s(self):
        if not 'id' in self.j_cch:
            print(self.j_cnf['name'] + ' not created')
            return 1

        self.cli.start(self.j_cch['id'])
        print('Started ' + self.j_cnf['name'])
        return 0

    def t(self):
        if not 'id' in self.j_cch:
            print(self.j_cnf['name'] + ' not created')
            return 1

        self.cli.stop(self.j_cch['id'])
        print('Stopped ' + self.j_cnf['name'])
        return 0

    def r(self):
        if not 'id' in self.j_cch:
            print(self.j_cnf['name'] + ' not created')
            return 1

        self.cli.remove_container(container = self.j_cch['id'])
        self.j_cch.pop('id')
        print('Removed ' + self.j_cnf['name'])

        return 0

    def p(self):
        print('P')
        return 0

    def b(self):
        print('B')
        return 0
