from ansible.module_utils.basic import * 

import sys

DOCUMENTATION = """
---
module: daemontools_svc
short_description: This module deploys services under daemontools/svc
"""

"""
For the test/debug cycle ansible provides ansible/hacking/test-module in their repository located at http://github.com/ansible/ansible

You can run with the following command:

```
>> ansible/hacking/test-module -m collaborative_filtering/deploy/daemontools_svc.py -a '{"state": "started", "setup_cmd": "export APP_ENVIRONMENT=stage;", "virtualenv": "/opt/local/venv/collaborative_filtering", "user": "cfuser", "args": {"lookupd-http-address": "127.0.0.1:4151"}, "exec_path": "/opt/collaborative_filtering/collaborative_filtering.py", "name": "collaborative_filtering", "count": 5}'
```

This will generate a file at ~/.ansible_module_generated you can then invoke with python to see how it runs:

```
python ~/.ansible_module_generated    
```

You'll need to re-generate the module each time you make a change. 

Documentation about this process can be found here: 
 * https://github.com/ansible/ansible/tree/devel/hacking
 * http://docs.ansible.com/ansible/developing_modules.html
 * (example) https://github.com/ansible/ansible-modules-core/blob/devel/commands/command.py

You can find documentation about the actual daemontools/svc implementation here: 
https://cr.yp.to/daemontools/faq/create.html

"""

RUN = """
#!/bin/sh
exec 2>&1;
{setup_cmd}s
{chuser}s {interpreter}s {exec_path}s {args}s
"""

LOG = """
#!/bin/sh
exec {chuser}s multilog t ./main
"""
def test_writeable(path, module): 
    try:
        with open('{}/test'.format(path), 'w+'):
            pass
        os.unlink('{}/test'.format(path))
    except OSError:
        module.fail_json(
                msg="{} should exist and be writeable by the deploy user".format(path)) 

def main():
    module = AnsibleModule(
        argument_spec = {
            'state': {'default': 'started', 'choices': ['started', 'stopped']},
            'setup_cmd': {}, 
            'virtualenv': {},
            'user': {},
            'args': {'type': 'dict'},
            'exec_path': {'required': True},
            'name': {'required': True},
            'count': {'default': 1, 'type': 'int'},
        }
    )

    state = module.params['state']
    setup_cmd = module.params['setup_cmd']
    virtualenv = module.params['virtualenv']
    user = module.params['user']
    args = module.params['args']
    exec_path = module.params['exec_path']
    name = module.params['name']
    count = module.params['count']

    if exec_path.strip() == "":
        module.fail_json(msg="The path to clone your service is required.")
    if name.strip() == "":
        module.fail_json(msg="You must name your service.")
    if not isinstance(count, int):
        module.fail_json(msg="Count must be the number of instances of your daemon to run.")
    if state not in ('started', 'stopped'):
        module.fail_json(msg="State should be either 'started' or 'stopped'")

    chuser = "setuidgid {}".format(user.strip()) if user.strip() else ""
    interpreter = "{}/bin/python".format(virtualenv.strip()) if virtualenv.strip() else sys.executable
    exec_path = exec_path.strip()
    args = " ".join(["--{}={}".format(k, v) for k, v in args.items()])

    run = RUN.format(setup_cmd=setup_cmd, 
            chuser=chuser, 
            interpreter=interpreter, 
            exec_path=exec_path, 
            args=args) 
    log = LOG.format(chuser=chuser)

    """
    TODO: 
    * Test setup command?  
    """
    if state == 'started':
        # Check for writeablility of local path to copy daemon to. /collaborative_filtering/service
        test_writeable('/collaborative_filtering/local', module)
        # Check writeability of path to install run script (that references the daemon script in the run command)
        test_writeable('/collaborative_filtering/service', module)
        # Check that we can link in /service
        test_writeable('/service')
        # Check that the user exists and make the copy of our daemon executable by them
    else:
        pass # TODO: Remove the service

    module.exit_json(changed=True, **{
        'run': run, 'log': log
    })

if __name__ == '__main__':
    main()
