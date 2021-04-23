# Contributing to CommFile

Communication File System

## Setting-Up Development environment

- Start by Forking [https://github.com/Wolverin-e/CommFile](https://github.com/Wolverin-e/CommFile) to yourusername.
- Docker must be installed.
- Install [Vscode-Remote-ExtentionPack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack).

```sh
# Clone your forked repository locally
$ git clone git@github.com:<yourusername>/CommFile.git

# Enter the local directory
$ cd CommFile

# Open in VSCode
$ code .

# Click on "Reopen in Container"

# Add Upstream
$ git remote add upstream https://github.com/Wolverin-e/CommFile.git

# Create a Virtual env: venv
$ python3 -m venv ./venv

# Activate venv
$ source venv/bin/activate

# Install The Project
$ pip install -e '.[dev]'

# Copy to config.json & fill it
$ cd ./MailFile
$ cp config.example.json config.json
$ code ./config.json

# Test the installation by
$ cd ..
$ mm ./mail_drive

# In another terminal
$ echo "Hello Testing World!" >> mail_drive
```

## Proposing new changes

```sh
# Update the local master
$ git checkout master
$ git fetch upstream
$ git rebase upstream/master

# Shift onto a new branch from the Master
$ git checkout -b <new-branch-name>


#########################
###   Do.Your.Magic   ###
#########################


# Before Commiting your code
# For Checking PEP8 Violations:
$ flake8 .
# If any violations -> For auto-linting:
$ autopep8 -i <file-to-lint>

# Commit Your Code
$ git add .
$ git commit -m '<good-commit-message>'

# Push your changes from the current branch to create a new branch with the same name
$ git push origin <new-branch-name>

# Create a Pull Request(PR): <your-remote>:<new-branch-name> → Wolverin-e:master
```
