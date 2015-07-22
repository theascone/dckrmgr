import os
import sys
import json
import docker
import argparse

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

        cli = docker.Client('unix://var/run/docker.sock')

        self.p_cwd = os.getcwd()
        self.p_cnf = os.path.join(self.p_cwd, 'dckrcnf.json')

        try:
            f_cnf = open(self.p_cnf, 'r')
        except OSError:
            print('Couldn\'t open dckrcnf.json')
            exit(1)

        self.j_cnf = json.load(f_cnf)

        for command in args.commands:
            if getattr(self, command)() != 0:
                exit(1)

        exit(0)

    def c(self):
        print('C')
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
