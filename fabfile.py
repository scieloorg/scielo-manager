# coding: utf-8
from fabric.api import (
    task,
    run,
    cd,
    prefix,
    sudo,
)
from fabric.context_managers import settings

import fabfile_settings as app_settings


@task
def restart_ws():
    """
    Restart the remote Web Server.
    """
    cmd = '%s' % app_settings.WEBSERVICE_RESTART_CMD
    with settings(warn_only=True):
        response_buff = run(cmd, combine_stderr=False)
        if response_buff.stderr:
            sudo(cmd)


@task
def update():
    """
    Update an instance running on a remote server.
    """
    with cd(app_settings.INSTALLATION_PATH):
        with prefix('source %s/bin/activate' % app_settings.VENV_PATH):
            run('git pull origin master')
            run('make upgrade')

    restart_ws()
