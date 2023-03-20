#!/usr/bin/python3
import argparse
import sys
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--version', action='version', version='%(prog)s v0.1')
subparsers = parser.add_subparsers(help='sub-command help')

parser_a = subparsers.add_parser('newproject', help='newproject proj flavour')
parser_a.add_argument('--nome',type=str,nargs=1)
parser_a.add_argument('--flavour',type=str,nargs='?',default='small')
parser_a.add_argument('--admin',type=str,nargs='?',default='batatas')

parser_b = subparsers.add_parser('delproject', help='--delproject project')
parser_b.add_argument('--delproject',type=str,nargs='?',default=argparse.SUPPRESS, metavar=('projeto'))
args = parser.parse_args()

print(f'{args}')

def results():
    return parser.parse_args()


def printVars():
    res = results()
    print("url          = {}".format(res.url))


def main():
    name=args.nome[0]
    flavour=args.flavour
    new_project(name,flavour)

def del_project(name):
    print(f'Projeto a ser eliminado:{name}\n')
    subprocess.run([f'oc delete project {name}'],shell=True, check=True)


def new_project(proj,flavour):
    print(f' Name:{proj} FLV:{flavour}')
    subprocess.run([f'oc apply -f project-templates/template-{flavour}.yaml -n openshift-config'],shell=True, check=True)
    subprocess.run([f'oc new-project {proj}'],shell=True, check=True)
    if (args.admin != 'batatas'):
        grant_admin_to_project(args.admin,proj)

def grant_admin_to_project(username, proj):
    subprocess.run([f'oc adm policy add-role-to-user admin {username} -n {proj}'],shell=True, check=True)
    #user=subprocess.run([f'oc whoami'],shell=True,text=True,capture_output=True).stdout.strip()
    user=subprocess.Popen([f'oc whoami'],shell=True,bufsize=64,stdout=subprocess.PIPE).stdout.readlines()[0].strip().decode('utf-8')
    #user=user.stdout.readlines()[0]
    #user=user.strip().decode('utf-8')
    subprocess.run([f'oc adm policy remove-role-from-user admin {user} -n {proj}'],shell=True, check=True)
main()
