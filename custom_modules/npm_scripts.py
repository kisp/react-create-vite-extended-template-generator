#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import json


def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type='str', required=True),
            name=dict(type='str', required=True),
            command=dict(type='str', required=False),
            status=dict(type='str', required=False, choices=['present', 'absent'], default='present')
        )
    )

    path = module.params['path']
    name = module.params['name']
    command = module.params['command']
    status = module.params['status']

    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        module.fail_json(msg=f"File '{path}' not found")

    scripts = data.get('scripts', {})

    if status == 'present':
        if name in scripts and scripts[name] == command:
            module.exit_json(changed=False, msg=f"Script '{name}' with command '{command}' already exists")
        scripts[name] = command
    elif status == 'absent' and not name in scripts:
        module.exit_json(changed=False, msg=f"Script '{name}' does not exist")
    elif status == 'absent' and name in scripts:
        del scripts[name]

    data['scripts'] = scripts

    try:
        with open(path, 'w') as file:
            json.dump(data, file, indent=2)
            file.write('\n')  # Ensure file ends with a newline
    except Exception as e:
        module.fail_json(msg=f"Failed to write to file '{path}': {e}")

    module.exit_json(changed=True, msg=f"Script '{name}' is now {status}")


if __name__ == '__main__':
    main()
