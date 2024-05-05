#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import subprocess
import os

def run_prettier(module, path, chdir, prettier_cmd):
    try:
        # Change the working directory if specified
        if chdir:
            os.chdir(chdir)

        # Run prettier command
        if prettier_cmd:
            cmd = prettier_cmd.split() + ['--write', path]
        else:
            cmd = ['prettier', '--write', path]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if there are changes
        if "unchanged" in result.stdout:
            return True, None
        else:
            return False, result.stdout.strip()
    except Exception as e:
        return False, str(e)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type='str', required=True),
            chdir=dict(type='str', required=False),
            prettier_cmd=dict(type='str', required=False)
        )
    )

    path = module.params['path']
    chdir = module.params.get('chdir')
    prettier_cmd = module.params.get('prettier_cmd')

    changed, output = run_prettier(module, path, chdir, prettier_cmd)

    if changed:
        module.exit_json(changed=False, msg="No changes")
    else:
        module.exit_json(changed=True, msg="File was formatted with prettier")

if __name__ == '__main__':
    main()
