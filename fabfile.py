"""
Starter fabfile for deploying the toolhub project.

Change all the things marked CHANGEME. Other things can be left at their
defaults if you are happy with the default layout.
"""
import os
import posixpath

from fabric.api import run, local, env, settings, cd, task
from fabric.contrib.files import exists
from fabric.operations import _prefix_commands, _prefix_env_vars
from fabric import colors
# from fabtools.vagrant import vagrant
#from fabric.decorators import runs_once
#from fabric.context_managers import cd, lcd, settings, hide


# CHANGEME
env.hosts = ['user@toolhub.example.com']
env.code_dir = '/srv/www/toolhub'
env.project_dir = '/srv/www/toolhub/toolhub'
env.static_root = '/srv/www/toolhub/static/'
env.virtualenv = '/srv/www/toolhub/.virtualenv'
env.code_repo = 'git@github.com:destos/toolhub.git'
env.django_settings_module = 'toolhub.settings'

# Python version
PYTHON_BIN = "python2.7"
PYTHON_PREFIX = ""  # e.g. /usr/local  Use "" for automatic
PYTHON_FULL_PATH = "%s/bin/%s" % (PYTHON_PREFIX, PYTHON_BIN) if PYTHON_PREFIX else PYTHON_BIN

# Set to true if you can restart your webserver (via wsgi.py), false to stop/start your webserver
# CHANGEME
DJANGO_SERVER_RESTART = False


def virtualenv(venv_dir):
    """
    Context manager that establishes a virtualenv to use.
    """
    return settings(venv=venv_dir)


def run_venv(command, **kwargs):
    """
    Runs a command in a virtualenv (which has been specified using
    the virtualenv context manager
    """
    run("source %s/bin/activate" % env.virtualenv + " && " + command, **kwargs)


def install_dependencies():
    ensure_virtualenv()
    with virtualenv(env.virtualenv):
        with cd(env.code_dir):
            run_venv("pip install -r requirements/production.txt")


def ensure_virtualenv():
    if exists(env.virtualenv):
        return

    with cd(env.code_dir):
        run("virtualenv --no-site-packages --python=%s %s" %
            (PYTHON_BIN, env.virtualenv))
        run("echo %s > %s/lib/%s/site-packages/projectsource.pth" %
            (env.project_dir, env.virtualenv, PYTHON_BIN))


def ensure_src_dir():
    if not exists(env.code_dir):
        run("mkdir -p %s" % env.code_dir)
    with cd(env.code_dir):
        if not exists(posixpath.join(env.code_dir, '.git')):
            run('git clone %s .' % (env.code_repo))


def push_sources():
    """
    Push source code to server
    """
    ensure_src_dir()
    local('git push origin master')
    with cd(env.code_dir):
        run('git pull origin master')


@task
def run_tests():
    """ Runs the Django test suite as is.  """
    local("./manage.py test")


@task
def version():
    """ Show last commit to the deployed repo. """
    with cd(env.code_dir):
        run('git log -1')


@task
def uname():
    """ Prints information about the host. """
    run("uname -a")


@task
def webserver_stop():
    """
    Stop the webserver that is running the Django instance
    """
    run("service apache2 stop")


@task
def webserver_start():
    """
    Starts the webserver that is running the Django instance
    """
    run("service apache2 start")


@task
def webserver_restart():
    """
    Restarts the webserver that is running the Django instance
    """
    if DJANGO_SERVER_RESTART:
        with cd(env.code_dir):
            run("touch %s/wsgi.py" % env.project_dir)
    else:
        with settings(warn_only=True):
            webserver_stop()
        webserver_start()


def restart():
    """ Restart the wsgi process """
    with cd(env.code_dir):
        run("touch %s/toolhub/wsgi.py" % env.code_dir)


def build_static():
    assert env.static_root.strip() != '' and env.static_root.strip() != '/'
    with virtualenv(env.virtualenv):
        with cd(env.code_dir):
            run_venv("./manage.py collectstatic -v 0 --clear --noinput")

    run("chmod -R ugo+r %s" % env.static_root)


@task
def first_deployment_mode():
    """
    Use before first deployment to switch on fake south migrations.
    """
    env.initial_deploy = True


@task
def update_database(app=None):
    """
    Update the database (run the migrations)
    Usage: fab update_database:app_name
    """
    with virtualenv(env.virtualenv):
        with cd(env.code_dir):
            if getattr(env, 'initial_deploy', False):
                run_venv("./manage.py syncdb --all")
                run_venv("./manage.py migrate --fake --noinput")
            else:
                run_venv("./manage.py syncdb --noinput")
                if app:
                    run_venv("./manage.py migrate %s --noinput" % app)
                else:
                    run_venv("./manage.py migrate --noinput")


@task
def sshagent_run(cmd):
    """
    Helper function.
    Runs a command with SSH agent forwarding enabled.

    Note:: Fabric (and paramiko) can't forward your SSH agent.
    This helper uses your system's ssh to do so.
    """
    # Handle context manager modifications
    wrapped_cmd = _prefix_commands(_prefix_env_vars(cmd), 'remote')
    try:
        host, port = env.host_string.split(':')
        return local(
            "ssh -p %s -A %s@%s '%s'" % (port, env.user, host, wrapped_cmd)
        )
    except ValueError:
        return local(
            "ssh -A %s@%s '%s'" % (env.user, env.host_string, wrapped_cmd)
        )


@task
def deploy():
    """
    Deploy the project.
    """
    with settings(warn_only=True):
        webserver_stop()
    push_sources()
    install_dependencies()
    update_database()
    build_static()
    webserver_start()


# FabFile from django-salted

import os
import hashlib
# Local paths
LOCAL_ROOT = os.path.dirname(os.path.realpath(__file__))


# Server paths
PROJECT_NAME = "example"
PROJECT_PATH = "/vagrant/toolhub"

MANAGE_BIN = "/vagrant/toolhub/manage.py"
VENV_PATH = "/home/vagrant/env"
WHEEL_PATH = "/home/vagrant/wheel"
WHEEL_NAME = "wheel-requirements.tar.gz"


def _md5_for_file(filename, block_size=2**20):
    filename = os.path.join(LOCAL_ROOT, filename)
    f = open(filename)
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    f.close()
    return md5.hexdigest()


@task
def manage_py(command):
    """ Runs a manage.py command on the server """
    run('{python} {manage} {command}'.format(python=VENV_PATH + "/bin/python",
                                             manage=MANAGE_BIN,
                                             command=command))


@task
def syncdb():
    """ Django syncdb command."""
    manage_py("syncdb --noinput")


@task
def migrate():
    """ Django South migrate command."""
    manage_py("migrate")


@task
def collectstatic():
    """ Run collectstatic command. """
    manage_py("collectstatic --noinput")


@task
def wheel():
    """ Create new wheel requirements file """
    # Get all the requirements
    print colors.green("Downloading and compiling requirements. This could take several minutes...")
    sudo('{pip} wheel --wheel-dir={wheel} -r {example}/requirements.txt'.format(pip=VENV_PATH + "/bin/pip",
                                                                                wheel=WHEEL_PATH + '/' + PROJECT_NAME,
                                                                                example=PROJECT_PATH),
         user="www-data",
         quiet=False)

    # Zip up
    print colors.green("Zipping all the requirements into one file...")
    with cd(WHEEL_PATH):
        sudo('tar czf {name} {project}/'.format(name=WHEEL_NAME,
                                                project=PROJECT_NAME),
             user="www-data",
             quiet=False)
        sudo('mv {name} /vagrant/'.format(name=WHEEL_NAME),
             quiet=False)

    # Create a MD5
    md5 = _md5_for_file(WHEEL_NAME)
    print colors.green('Upload the requirements and set the following MD5 in your pillar configuration: {md5}'.format(md5=md5))
