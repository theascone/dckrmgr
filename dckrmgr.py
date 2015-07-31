import os
import sys
import json
import docker
import argparse
import importlib
import jsonschema

commands = {}

def read_json(pth, sch=None):
    bsn = os.path.basename(pth)

    try:
        f_jsn = open(pth, 'r')
    except FileNotFoundError:
        print('Couldn\'t open ' + bsn + ': Not found')
        exit(1)
    except PermissionError:
        print('Couldn\'t open ' + bsn + ': Insufficient rights')
        exit(1)
    except OSError:
        print('Couldn\'t open ' + bsn)
        exit(1)

    try:
        jsn = json.load(f_jsn)
    except ValueError:
        print('Couldn\'t deserialize ' + bsn + ': Invalid json')
        exit(1)
    finally:
        f_jsn.close()

    if sch is not None:
        try:
            jsonschema.validate(jsn, sch)
        except jsonschema.exceptions.SchemaError:
            print('Couldn\'t validate ' + bsn + ': Invalid schema')
            exit(1)
        except jsonschema.exceptions.ValidationError as error:
            print('Couldn\'t accept '+ bsn + ': ' + error.message)
            exit(1)

    return jsn

def main():
    cli = docker.Client('unix://var/run/docker.sock')

    p_src = os.path.dirname(os.path.abspath(__file__))
    p_s_cnf = os.path.join(p_src, 'dckrcnf.schema.json')

    for file in os.listdir(os.path.join(p_src, 'commands')):
        ext_file = os.path.splitext(file)

        if ext_file[1] == '.py' and not ext_file[0] == '__init__':
            importlib.import_module('commands.' + ext_file[0])

    parser = argparse.ArgumentParser()
    parser.add_argument('-D', dest='cwd_root', action='store', default='', help='Set working directory')
    parser.add_argument('-R', dest='rec', action='store_true', help='Use dckrsub.json files to recursively apply operations')

    for cm in commands.items():
        parser.add_argument('-' + cm[0], dest='commands', action='append_const', const=cm[0], help=cm[1]['help'])

    args = parser.parse_args()

    p_cwd = os.path.join(os.getcwd(), args.cwd_root)
    p_cnf = os.path.join(p_cwd, 'dckrcnf.json')

    j_sch = read_json(p_s_cnf)
    j_cnf = read_json(p_cnf, j_sch)

    i_sts = 0

    for command in args.commands:
        if commands[command]['func'](cli, p_cwd, j_cnf) != 0:
            i_sts = 1
            break

    exit(i_sts)
