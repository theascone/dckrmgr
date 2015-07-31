import os
import sys
import json
import docker
import argparse
import importlib
import jsonschema

commands = {}

def main():
    cli = docker.Client('unix://var/run/docker.sock')

    p_src = os.path.dirname(os.path.abspath(__file__))

    for file in os.listdir(os.path.join(p_src, 'commands')):
        ext_file = os.path.splitext(file)

        if ext_file[1] == '.py' and not ext_file[0] == '__init__':
            importlib.import_module('commands.' + ext_file[0])

    parser = argparse.ArgumentParser()
    parser.add_argument('-D', dest='cwd_root', action='store', default=os.getcwd(), help='Set working directory')
    parser.add_argument('-R', dest='rec', action='store_true', help='Use dckrsub.json files to recursively apply operations')

    for cm in commands.items():
        parser.add_argument('-' + cm[0], dest='commands', action='append_const', const=cm[0], help=cm[1]['help'])

    args = parser.parse_args()

    p_cwd = os.path.join(os.getcwd(), args.cwd_root)
    p_cnf = os.path.join(p_cwd, 'dckrcnf.json')

    try:
        f_cnf = open(p_cnf, 'r')
    except OSError:
        print('Couldn\'t open dckrcnf.json')
        exit(1)

    try:
        f_sch = open(os.path.join(p_src, 'dckrcnf.schema.json'), 'r')
    except OSError:
        print('Couldn\'t open dckrcnf.schema.json')
        exit(1)

    try:
        j_cnf = json.load(f_cnf)
    except ValueError:
        print('dckrcnf.json is invalid json')
        exit(1)

    try:
        j_sch = json.load(f_sch)
    except ValueError:
        print('dckrcnf.schema.json is invalid json')
        exit(1)

    try:
        jsonschema.validate(j_cnf, j_sch)
    except jsonschema.exceptions.ValidationError as detail:
        print(detail.message)
        exit(1)

    i_sts = 0

    for command in args.commands:
        if commands[command]['func'](cli, p_cwd, j_cnf) != 0:
            i_sts = 1
            break

    exit(i_sts)
