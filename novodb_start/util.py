import socket
import subprocess as sp
from pathlib import Path

import click


def check_port(port):
    """
    检查指定端口是否被占用，如占用，则+1
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        while True:
            if s.connect_ex(('localhost', port)) == 0:
                click.secho(f'port is alreay in use: {port}', fg='yellow')
                port += 1
            else:
                click.secho(f'port is available: {port}', fg='green')
                return port


def run_cmd(cmd):
    click.secho(f'>>> run cmd: {cmd}', fg='cyan')
    res = sp.run(cmd, shell=True, capture_output=True)
    if res.returncode != 0:
        raise Exception(f'ERR: {res.stderr}')
    return res.stdout


def write_file(file, content):
    with Path(file).open('w') as out:
        out.write(content.strip() + '\n')
    click.secho(f'>>> write file: {file}')
