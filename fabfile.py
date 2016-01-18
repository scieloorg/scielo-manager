# coding: utf-8
""" Tarefas para manutenção de instalações do SciELO Manager.

Exemplo:
    fab deploy:tag=v2016.01.18 --scielomanager_settings_file=/etc/scieloapps/scielomanager.py \
--installation_path=/var/www/manager_scielo_org
"""
from fabric.api import *


SCIELOMANAGER_SETTINGS_FILE = env.get('scielomanager_settings_file',
        '/etc/scieloapps/scielomanager.py')
INSTALLATION_PATH = env.get('installation_path',
        '/var/www/manager_scielo_org')


def get_version():
    """ Obtém a versão ativa da instalação.

    O formato da resposta segue a máscara:

        <tag>-<total de commits além da tag>-<hash do head>


    Veja https://www.git-scm.com/docs/git-describe
    """
    with cd(INSTALLATION_PATH):
        output = run('git describe --long --dirty --abbrev=10 --tags')
        return output


def list_watchers():
    """ `watcher` é uma entidade monitorada pelo Circus.

    Cada `watcher` pode ser composto por 1 ou N processos.
    """
    with settings(sudo_user='root', warn_only=True):
        output = sudo('circusctl status | grep scielomanager')
        return [line.split(':')[0] for line in output.splitlines()]


def reload_app():
    """ Reinicia, com carinho, todos os `watchers` da aplicação.
    """
    with settings(sudo_user='root', warn_only=True):
        for watcher in list_watchers():
            sudo('circusctl reload %s' % watcher)


def kill_circus():
    """ Termina o Circus e todos os seus `watchers`.

    Tendo em vista que o `circusd` é gerenciado pelo monitor do sistema operacional,
    essa função funciona como um `reload` do tipo força-bruta e deve ser evitado
    pois causa indisponibilidade da app.
    """
    with settings(sudo_user='root', warn_only=True):
        sudo('circusctl quit')


def deploy(tag):
    """ Instala a versão `tag` da aplicação.
    """
    with settings(sudo_user='root', warn_only=True):
        with settings(warn_only=True):
            if run('test -d {path}'.format(path=INSTALLATION_PATH)).failed:
                sudo('git clone https://github.com/scieloorg/scielo_publishing_schema.git {path}'.format(
                    path=INSTALLATION_PATH))

        with cd(INSTALLATION_PATH):
            with prefix('workon scielomanager'):
                sudo('git fetch origin && git checkout {tag} -b {tag}'.format(
                    tag=tag))
                sudo('SCIELOMANAGER_SETTINGS_FILE={path} make upgrade'.format(
                    path=SCIELOMANAGER_SETTINGS_FILE))

    reload_app()


def backup_db():
    """ Realiza *dump* completo da base de dados da aplicação.
    """
    pass

def restore_db(path_to_script):
    """ Realiza *restore* da base de dados, com base no script SQL disponível em
    `path_to_script`.
    """
    pass

