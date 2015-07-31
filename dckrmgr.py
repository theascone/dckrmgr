import os
import sys
import docker
import dckrjsn
import argparse
import importlib

cli = None

p_cwd_top = None

n_cnf = 'dckrcnf.json'
n_sub = 'dckrsub.json'
n_s_cnf = 'dckrcnf.schema.json'
n_s_sub = 'dckrsub.schema.json'

p_src = os.path.dirname(os.path.abspath(__file__))
p_s_cnf = os.path.join(p_src, n_s_cnf)
p_s_sub = os.path.join(p_src, n_s_sub)

s_cnf = dckrjsn.read_json(p_s_cnf)
s_sub = dckrjsn.read_json(p_s_sub)

m_cmd = {}

def addCtx(p_cwd, a_ctx):
    p_cnf = os.path.join(p_cwd, n_cnf)
    cnf = dckrjsn.read_json(p_cnf, sch = s_cnf)

    a_ctx.append({
        'p_cwd': p_cwd,
        'cnf': cnf
    })

def recursiveCtx_i(p_cwd, a_ctx):
    p_sub = os.path.join(p_cwd, n_sub)
    a_sub = dckrjsn.read_json(p_sub, sch = s_sub)

    for sub in a_sub:
        if 'folder' in sub:
            p_cwd_nxt = os.path.join(p_cwd, sub['folder'])
            recursiveCtx_i(p_cwd_nxt, a_ctx)
        else:
            addCtx(p_cwd, a_ctx)

def recursiveCtx():
    a_ctx = []
    recursiveCtx_i(p_cwd_top, a_ctx)
    return a_ctx

def directCtx():
    a_ctx = []
    addCtx(p_cwd_top, a_ctx)
    return a_ctx

def main():
    global cli
    global p_cwd_top

    cli = docker.Client('unix://var/run/docker.sock')

    for file in os.listdir(os.path.join(p_src, 'commands')):
        ext_file = os.path.splitext(file)

        if ext_file[1] == '.py' and not ext_file[0] == '__init__':
            importlib.import_module('commands.' + ext_file[0])

    parser = argparse.ArgumentParser()
    parser.add_argument('-D', dest='p_cwd_top', action='store', default='', help='Set working directory')
    parser.add_argument('-R', dest='rec', action='store_true', help='Use dckrsub.json files to recursively apply operations')

    for cmd in m_cmd.items():
        parser.add_argument('-' + cmd[0], dest='a_cmd', action='append_const', const=cmd[0], help=cmd[1]['hlp'])

    args = parser.parse_args()

    p_cwd_top = os.path.join(os.getcwd(), args.p_cwd_top)

    if args.rec:
        a_ctx = recursiveCtx()
    else:
        a_ctx = directCtx()

    for cmd in args.a_cmd:
        if m_cmd[cmd]['ord'] == 'nrm':
            i_ctx = a_ctx
        elif m_cmd[cmd]['ord'] == 'rev':
            i_ctx = reversed(a_ctx)
        else:
            exit(1)

        for ctx in i_ctx:
            if m_cmd[cmd]['fnc'](ctx) != 0:
                exit(1)

    exit(0)
