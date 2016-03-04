from ansible.module_utils.basic import * 

import os
import pwd
import hashlib

DOCUMENTATION = """
---
module: daemontools_svc
author: Andrew Kelleher <keats.kelleher@gmail.com>
short_description: This module deploys services under daemontools/svc
options:
    state:
        description: The desired state of the service. Options are 'started' or 'absent'
        required: true
    setup_cmd:
        description: The command to configure the environment in which the daemon will run.
        required: false
    user:
        description: The unprivileged user who will run the daemon
        required: false
    run_cmd:
        description: The command to invoke your service. NOTE: The service should run in the foreground. Be sure to invoke the one in the local directory, not your code repository.
        required: true
    daemon_path:
        description: The path to the standalone file or directory from which your service will be copied.
        required: true
    name:
        description: A human readable name for your service that will be used to prefix it in the /service directory
        required: true
    count:
        description: The number of instances of the service to run.
        required: true
"""

EXAMPLES = """
name: "Install collaborative_filtering service"
daemontools_svc:
    state=started
    setup_cmd="export APP_ENVIRONMENT=dev"
    user=cfuser
    run_cmd="/local/venv/collaborative_filtering/bin/python /collaborative_filtering/local/collaborative_filtering.py"
    daemon_path="/opt/personal/collaborative_filtering/collaborative_filtering.py"
    name=collaborative_filtering
    count=2
"""

"""
For this project we have these defined statically. To generalize this we should allow these values
to be passed as parameters
"""
LOCAL_DIRECTORY = '/collaborative_filtering/local'
LOCAL_SERVICE_DIRECTORY = '/collaborative_filtering/service'
DAEMONTOOLS_SERVICE_DIRECTORY = '/service'


RUN = """
#!/bin/sh
exec 2>&1;
{setup_cmd}
{chuser} {run_cmd}
"""

LOG = """
#!/bin/sh
exec {chuser} multilog t ./main
"""


def test_writeable(path, module): 
    try:
        with open('{}/test'.format(path), 'w+'):
            pass
        os.unlink('{}/test'.format(path))
    except OSError:
        module.fail_json(
                msg="{} should exist and be writeable by the deploy user".format(path)) 


def export_daemon(module, daemon_path):
    rc, stdout, stderr = module.run_command("rsync -a --copy-dirlinks --delete {} {}".format(daemon_path, LOCAL_DIRECTORY))
    if rc:
        module.fail_json(msg="Rsync failed to copy the daemon application.")
    if stdout.strip():
        return True
    return False


def create_directory(path):
    if os.path.exists(path):
        return False
    os.makedirs(path)
    return True


def write_file(filepath, contents):
    before = ""
    try:
        with open(filepath, 'rb') as fp:
            before = hashlib.sha1(fp.read()).hexdigest
    except IOError:
        pass

    after = hashlib.sha1(contents).hexdigest
    if before != after:
        with open(filepath, 'w+') as fp:
            fp.write(contents)
            os.chmod(filepath, '0755')
        return True
    return False


def create_symlink(source, link_name):
    try:
        os.symlink(source, link_name)
    except OSError:
        return False
    return True


def main():
    module = AnsibleModule(
        argument_spec = {
            'state': {'default': 'started', 'choices': ['started', 'absent']},
            'setup_cmd': {},
            'user': {},
            'run_cmd': {'required': True},
            'daemon_path': {'required': True},
            'name': {'required': True},
            'count': {'default': 1, 'type': 'int'},
        }
    )

    state = module.params['state']
    setup_cmd = module.params['setup_cmd']
    user = module.params['user']
    run_cmd = module.params['run_cmd']
    daemon_path = module.params['daemon_path']
    name = module.params['name']
    count = module.params['count']

    if daemon_path.strip() == "" or not os.path.exists(daemon_path.strip()):
        module.fail_json(msg="The path to your service is required.")
    if name.strip() == "":
        module.fail_json(msg="You must name your service.")
    if not isinstance(count, int):
        module.fail_json(msg="Count must be the number of instances of your daemon to run.")
    if state not in ('started', 'stopped'):
        module.fail_json(msg="State should be either 'started' or 'stopped'")

    chuser = "setuidgid {}".format(user.strip()) if user.strip() else ""
    daemon_path = daemon_path.strip()

    run = RUN.format(setup_cmd=setup_cmd, 
                     chuser=chuser,
                     run_cmd=run_cmd)
    log = LOG.format(chuser=chuser)

    changed = False
    if state == 'started':
        # Test whether or not the deploy will succeed before making any changes
        test_writeable(LOCAL_DIRECTORY, module)
        test_writeable(LOCAL_SERVICE_DIRECTORY, module)
        test_writeable(DAEMONTOOLS_SERVICE_DIRECTORY, module)
        if user.strip():
            try:
                pwd.getpwnam(user.strip())
            except KeyError:
                module.fail_json(msg="The user, {}, does not exist.".format(user.strip()))

        # Sync daemon application
        if export_daemon(module, daemon_path):
            changed = True

        # Install service to /service
        for i in xrange(count):
            service_directory = os.path.join(LOCAL_SERVICE_DIRECTORY, '{}-{}'.format(name, i))
            log_directory = os.path.join(service_directory, 'log')

            changed = any([
                create_directory(service_directory),
                create_directory(log_directory),
                write_file(os.path.join(service_directory, 'run'), run),
                write_file(os.path.join(log_directory, 'run'), log),
                create_symlink(service_directory,
                               os.path.join(DAEMONTOOLS_SERVICE_DIRECTORY, os.path.basename(service_directory)))
            ]) or changed
    else:
        return module.fail_json(msg="Removing services is not yet implemented. You have to do it manually.")

    module.exit_json(changed=changed)

if __name__ == '__main__':
    main()
