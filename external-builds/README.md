# rockbuilder

Rockbuilder provides a configuration file based way of building
one ore multiple projects. Project can be application, library or
some other buildable or installable source code.

Configuration files are stored in the projects-directory and there exist
2 types of configuration files.

## project list configuration files

project list configuration files can be used to store a list of projects
that are wanted to build at the same time. At the moment this is hardcoded
to be a projects/core_apps.cfg but it is planned that in future there
can be multiple different project lists.

## project configuration file

Project configuration file specifies actions executed for the project:
- checkout
- clean
- configure
- build
- install

If action is not specified, then by default checkout, configure, build and install actions.

There can be separate action commands for posix/linux based systems and dos/windows-based operating systems. 

If specific action is given instead of using the default (for example build), rockbuilder does not at the
moment check whether other actions like checkout are done for the project before that. This will likely
change in the future.

# usage

##  build and install all

source ./.venv/bin/activate
cd external-projects
python rockbuilder.py
    
## checkout all projects (without build and install)

python rockbuilder.py --checkout
    
## checkout only the pytorch_audio sources

python rockbuilder.py --checkout --project pytorch_audio
    
## build only pytorch audio

python rockbuilder.py --build --project pytorch_audio
    
## install only pytorch audio

python rockbuilder.py --install --project pytorch_audio
