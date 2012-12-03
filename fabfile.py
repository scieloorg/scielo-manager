# coding: utf-8
from fabric.api import (
    task,
    run,
    cd,
    prefix,
    sudo,
)
from fabric.context_managers import settings

from fabfile_settings import deploy_envs as app_settings


@task
def restart_ws(env):
    """
    Restart the remote Web Server.
    """
    if env not in app_settings:
        exit('unknown deploy environment. is it configured in fabfile_settings.py?')

    cmd = '%s' % app_settings[env]['webservice_restart_cmd']
    with settings(warn_only=True):
        response_buff = run(cmd, combine_stderr=False)
        if response_buff.stderr or 'permission denied' in response_buff.stdout.lower():
            sudo(cmd)


@task
def update(env):
    """
    Update an instance running on a remote server.
    """
    if env not in app_settings:
        exit('unknown deploy environment. is it configured in fabfile_settings.py?')

    with cd(app_settings[env]['installation_path']):
        with prefix('source %s/bin/activate' % app_settings[env]['venv_path']):
            # stash modifications to apply them later
            run('git stash')
            run('git pull origin master')
            run('git stash pop')
            run('make upgrade')

    restart_ws(env)
