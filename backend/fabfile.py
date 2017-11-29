from fabric.api import *


#
# Base configuration
#

env.project_name = 'bank'
env.path = '/home/ubuntu/sites/%(project_name)s' % env
env.env_path = '%(path)s/server/env' % env
env.repository_url = 'git@github.com:nelsonmonteiro/bank.git'
env.python = 'python2.7'
env.user = 'ubuntu'
env.use_varnish = False


#
# Environments
#
def production():
    """
    Work on production environment
    """
    env.settings = 'production'
    env.hosts = ['']
    env.key_filename = './keys/bank-dev.pem'


def staging():
    """
    Work on staging environment
    """
    env.settings = 'staging'
    env.hosts = ['']
    env.key_filename = './keys/bank-staging.pem'


#
# Branches
#
def master():
    """
    Work on stable branch (production server).
    """
    env.branch = 'master'


def branch(branch_name):
    """
    Work on any specified branch.
    """
    env.branch = branch_name


#
# Commands - setup
#
def setup():
    """
    Setup a fresh virtualenv, install everything we need

    Does NOT perform the functions of deploy().
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[master, branch])

    install_dependencies()
    clone_repo()
    collect_static()
    install_web_server()


#
# Commands - deployment
#
def deploy():
    """
    Deploy the latest version of the site to the server and restart nginx.

    Does not perform the functions of load_new_data().
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[staging, master, branch])

    checkout_latest(with_requirements=True)
    collect_static()
    restart_web_server()


def simple_deploy():
    """
    Deploy the latest version of the site to the server and restart nginx.
    Does not perform collect static neither setup symbolic links.
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[staging, master, branch])

    checkout_latest(with_requirements=False)
    restart_web_server()


#
# Commands - front-end
#
def build():
    """
    Deploy the latest version of the site to the server and restart nginx.

    Does not perform the functions of load_new_data().
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[staging, master, branch])

    run("cd %(path)s/app; ng build --prod" % env)


#
# Commands - rollback
#
def rollback(commit_id):
    """
    Rolls back to specified git commit hash or tag.

    There is NO guarantee we have committed a valid dataset for an arbitrary
    commit hash.
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[staging, master, branch])

    checkout_latest()
    git_reset(commit_id)


def git_reset(commit_id):
    """
    Reset the git repository to an arbitrary commit hash or tag.
    """
    env.commit_id = commit_id
    run("cd %(path)s; git reset --hard %(commit_id)s" % env)


#
# Commands - miscellaneous
#
def echo_host():
    """
    Echo the current host to the command line.
    """
    run('echo %(settings)s; echo %(hosts)s' % env)


#
# Commands - shared
#
def install_dependencies():
    sudo('apt-get install -y git nginx rabbitmq-server supervisor ruby-full rubygems-integration python-celery '
         'libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev '
         'tk8.6-dev python-tk npm postgresql postgresql-contrib python-pip postgresql-server-dev-all '
         'libxml2-dev libxslt1-dev python-dev python-lxml libffi-dev libxmlsec1-dev nodejs-legacy' % env)
    sudo('pip install virtualenv' % env)
    sudo('gem install css')
    sudo('gem install sass')
    sudo('npm -g install yuglify')


def clone_repo():
    """
    Do initial clone of the git repository.
    """
    run('git clone --recursive %(repository_url)s %(path)s' % env)
    run('virtualenv --no-site-packages %(env_path)s;' % env)
    checkout_latest(with_requirements=True)


def checkout_latest(with_requirements=False):
    """
    Pull the latest code on the specified branch.
    """
    run('cd %(path)s; git pull origin %(branch)s' % env)
    run('cd %(path)s; git submodule update' % env)
    run('cd %(path)s; git submodule sync' % env)
    if with_requirements:
        with prefix('source %(env_path)s/bin/activate' % env):
            run('pip install -r %(path)s/server/requirements.txt' % env)
    with prefix('source %(env_path)s/bin/activate' % env):
        run('python %(path)s/backend/configs/%(settings)s/manage.py migrate;' % env)


@with_settings(warn_only=True)
def collect_static():
    with prefix('source %(env_path)s/bin/activate' % env):
        run('python %(path)s/backend/configs/%(settings)s/manage.py collectstatic --noinput;' % env)


def install_web_server():
    run('mkdir -p %(path)s/logs/' % env)
    sudo('chown -R %(user)s:%(user)s %(path)s/logs/' % env)

    # SUPERVISOR
    sudo('rm -fr /etc/supervisor/conf.d/%(project_name)s.conf' % env)
    sudo('ln -s %(path)s/backend/configs/%(settings)s/supervisor.conf '
         '/etc/supervisor/conf.d/%(project_name)s.conf' % env)
    # sudo('ln -s %(path)s/backend/configs/%(settings)s/supervisor.conf /etc/default/celeryd' % env)
    sudo('chmod a+x %(path)s/backend/configs/%(settings)s/server.sh' % env)
    sudo('sudo supervisorctl reread')
    sudo('sudo supervisorctl update')

    # NGINX
    sudo('rm -fr /etc/nginx/sites-enabled/default' % env)
    sudo('rm -fr /etc/nginx/sites-enabled/%(project_name)s.conf' % env)
    sudo('ln -s %(path)s/backend/configs/%(settings)s/nginx.conf '
         '/etc/nginx/sites-enabled/%(project_name)s.conf' % env)
    restart_web_server()


def restart_web_server():
    """
    Restart the web servers.
    """
    sudo('/etc/init.d/nginx restart')
    sudo('/etc/init.d/supervisor restart')
    sudo('supervisorctl stop %(project_name)s' % env)
    sudo('supervisorctl start %(project_name)s' % env)
    # sudo('/etc/init.d/celeryd restart')
