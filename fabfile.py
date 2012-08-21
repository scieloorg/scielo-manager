# coding: utf-8
from fabric.api import (
    task,
    run,
    cd,
    prefix,
)

import fabfile_settings as settings


@task
def update():
    with cd(settings.INSTALLATION_PATH):
        with prefix('source %s/bin/activate' % settings.VENV_PATH):
            run('git pull origin master')
            run('make upgrade')
