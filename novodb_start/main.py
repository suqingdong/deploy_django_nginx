#!/usr/bin/env python
import sys
import getpass
from pathlib import Path

import click

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
sys.path.insert(0, str(BASE_DIR))

from novodb_start import config, util


CONTEXT_SETTINGS = dict(help_option_names=['-?', '-h', '--help'])


__epilog__ = click.style('''

\b
example:
    novodb_start \\
        -b /data2/work/linmeng/proj/novodb/beet/api/ \\        # 后端根目录
        -f /data2/work/linmeng/proj/novodb/beet/app/dist/ \\   # 前端dist目录
        -n demo \\                                             # 项目名称
        -p 1080 \\                                             # 网络端口[可不写，会自动检查]
        -d /data2/work/novodb \\                               # 生成根目录[可不写，默认都部署到这里]
''', fg='cyan')


@click.command(
    help=click.style('NovoDB前后端一键化部署工具', fg='green', bold=True),
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
    epilog=__epilog__,
)
@click.option('-f', '--front-end', help='the dist directory of front-end', required=True)
@click.option('-b', '--back-end', help='the build directory of back-end', required=True)
@click.option('-n', '--name', help='the name of project', required=True)
@click.option('-d', '--root', help='the root directory', default='/data2/work/novodb', show_default=True)
@click.option('-p', '--port', help='the port number', default=1080, show_default=True)
@click.option('-y', '--force', help='force overwrite directory', is_flag=True)
def main(**kwargs):
    root_dir = Path(kwargs['root']).resolve()

    proj_dir = root_dir.joinpath(kwargs['name'])
    if proj_dir.exists():

        if proj_dir.owner() != getpass.getuser():
            click.secho(f'[{proj_dir}]项目路径已存在，请检查或更换项目名称！', fg='red')
            exit(1)

        if not (kwargs['force'] or click.confirm('项目路径已存在，是否覆盖')):
            exit(1)

    api_root = proj_dir.joinpath('api')
    app_root = proj_dir.joinpath('app')

    front_end_dir = kwargs['front_end']
    back_end_dir = kwargs['back_end']

    port = util.check_port(kwargs['port'])

    util.run_cmd(f'mkdir -p {proj_dir}/{{logs,config}}')
    util.run_cmd(f'rsync -luvr --exclude nohup.out {front_end_dir}/* {app_root}')
    util.run_cmd(f'rsync -luvr --exclude nohup.out {back_end_dir}/* {api_root}')

    util.write_file(
        proj_dir.joinpath('config', 'nginx.conf'),
        config.nginx.format(PROJ_DIR=proj_dir, PORT=port,
                            API_ROOT=api_root, APP_ROOT=app_root),
    )

    util.write_file(
        proj_dir.joinpath('config', 'uwsgi.ini'),
        config.uwsgi.format(PROJ_DIR=proj_dir, API_ROOT=api_root),
    )

    util.write_file(
        proj_dir.joinpath('start.sh'),
        config.shell.format(PROJ_DIR=proj_dir),
    )

    util.write_file(
        proj_dir.joinpath('URL'),
        f'内网: http://172.18.11.93:{port}\n公网: http://117.78.45.2:{port}',
    )

    click.secho(f'''
        项目路径：\t{proj_dir}
        启动服务：\tsh {proj_dir.joinpath('start.sh')}
    ''', fg='cyan')


if __name__ == '__main__':
    main()
