#!/usr/bin/python3
'''fabric script for task 4 0X03'''

from fabric.api import local, put, run, env
from datetime import datetime
import re
from os import path


env.hosts = ['34.75.211.145', '3.236.217.0']


def do_pack():
    '''generates a .tgz archive from the contents of the web_static folder'''
    local("mkdir -p versions")
    path = "versions/web_static_{}.tgz".format(
                                        datetime.strftime(
                                                 datetime.now(),
                                                 "%Y%m%d%H%M%S"))
    result = local("tar -cvzf {} web_static"
                   .format(path),
                   capture=True)

    if result.failed:
        return None
    return path


def do_deploy(archive_path):
    '''distributes an archive to my web servers'''
    if not path.exists(archive_path):
        return False

    file_name = re.search(r'versions/(\S+).tgz', archive_path)
    if file_name is None:
        return False
    file_name = file_name.group(1)
    res = put(local_path=archive_path, remote_path="/tmp/{}.tgz"
              .format(file_name))
    if res.failed:
        return False

    res = run("mkdir -p /data/web_static/releases/{}".format(file_name))
    if res.failed:
        return False

    res = run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
              .format(file_name, file_name))
    if res.failed:
        return False

    res = run('rm -rf /tmp/{}.tgz'.format(file_name))
    if res.failed:
        return False

    res = run(('mv /data/web_static/releases/{}/web_static/* ' +
              '/data/web_static/releases/{}/')
              .format(file_name, file_name))
    if res.failed:
        return False

    res = run('rm -rf /data/web_static/releases/{}/web_static'
              .format(file_name))
    if res.failed:
        return False

    res = run('rm -rf /data/web_static/current')
    if res.failed:
        return False

    res = run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
              .format(file_name))
    if res.failed:
        return False

    print('New version deployed!')
    return True


def deploy():
    '''creates and distributes an archive to my web servers'''
    path = do_pack()
    if path is None:
        return False

    res = do_deploy(path)
    return res


def do_clean(number=0):
    '''deletes out-of-date archives'''
    local_files = local("ls -1t versions", capture=True)
    file_names = local_files.split("\n")
    n = 1 if int(number) <= 1 else int(number)

    for i in file_names[n:]:
        local("rm -rf versions/{}".format(i))

    server_files = run("ls -1t /data/web_static/releases")
    server_files_names = server_files.split("\n")

    for i in server_files_names[n:]:
        if i == 'test':
            continue
        run("rm -rf /data/web_static/releases/{}"
            .format(i))
