#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import subprocess
import os

def main():
    module = AnsibleModule(
        argument_spec=dict(
            subject=dict(type='str', required=True),
            chdir=dict(type='path', required=False),
            body=dict(type='str', required=False)
        )
    )

    subject = module.params['subject']
    body = module.params.get('body')
    chdir = module.params.get('chdir')

    try:
        # Change directory if specified
        if chdir:
            os.chdir(chdir)

        # Get git status
        git_status_output = subprocess.check_output(["git", "status"])

        # Check if commit already exists
        if "No commits yet" in git_status_output.decode():
            exists = False
        else:
            exists = subprocess.check_output(["git", "log", "--grep=" + subject])

        if exists:
            module.exit_json(changed=False, msg="Commit with that message already exists")
        else:
            # Check git status
            git_status_porcelain_output = subprocess.check_output(["git", "status", "--porcelain"])
            if not git_status_porcelain_output.strip():
                module.fail_json(msg="No changes to commit. Working tree is clean.")

            # Create the commit message
            if body:
                full_commit_message = "{}\n\n{}".format(subject, body)
            else:
                full_commit_message = subject

            # Add all files
            subprocess.check_call(["git", "add", "--all"])

            # Commit the changes
            if body:
                # Write the commit message to a temporary file
                with open('commit_message.txt', 'w') as file:
                    file.write(full_commit_message)
                subprocess.check_call(["git", "commit", "-F", "commit_message.txt"])
                os.remove("commit_message.txt")
            else:
                subprocess.check_call(["git", "commit", "-m", full_commit_message])

            module.exit_json(changed=True, msg="Commit made with message: {}".format(full_commit_message))
    except subprocess.CalledProcessError as e:
        module.fail_json(msg="Failed to execute git command: {}".format(e))
    finally:
        # Change back to the original directory if chdir was used
        if chdir:
            os.chdir(os.path.expanduser("~"))

if __name__ == '__main__':
    main()
