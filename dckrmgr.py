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

        self.p_cwd = os.getcwd()
        self.p_cnf = os.path.join(self.p_cwd, 'dckrcnf.json')

        try:
            f_cnf = open(self.p_cnf, 'r')
            f_sch = open('../dckrcnf.schema.json', 'r')
        except OSError:
            print('Couldn\'t open dckrcnf.json')
            exit(1)

        self.j_cnf = json.load(f_cnf)
        j_sch = json.load(f_sch)

        try:
            jsonschema.validate(self.j_cnf, j_sch)
        except jsonschema.exceptions.ValidationError as detail:
            print(detail.message)
            exit(1)

        for command in args.commands:
            if getattr(self, command)() != 0:
                exit(1)

        exit(0)

    def c(self):
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
            ports.append(port['container_port'])

            if 'address' in  port:
                port_bindings[port['container_port']] = (port['address'], port['host_port'])
            else:
                port_bindings[port['container_port']] = port['host_port']

        links = {}

        for link in self.j_cnf['links']:
            links[link['name']] = link['alias']

        host_config = docker.utils.create_host_config(
            binds = binds,
            port_bindings = port_bindings,
            links = links
        )

        try:
            self.cli.create_container(
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

        print('Created ' + self.j_cnf['name'])

        return 0

    def s(self):
        print('S')
        return 0

    def t(self):
        print('T')
        return 0

    def r(self):
        print('R')
        return 0

    def p(self):
        print('P')
        return 0

    def b(self):
        print('B')
        return 0

if __name__ == '__main__':
    DckrMgr()
