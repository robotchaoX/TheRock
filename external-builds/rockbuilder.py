#!/usr/bin/env python
#! python
import argparse
import configparser
import lib_python.project_builder as project_builder
import sys
import os
import time
import platform

def is_directory_in_path_env_variable(env_variable, directory):
  """
  Checks if a directory is in the env_variable environment variable.

  Args:
    env_variable: Environment variable used to check the path
    directory: The path searched from the environment variable

  Returns:
    True if the directory is in PATH, False otherwise.
  """
  path_env = os.environ.get(env_variable, '')
  path_directories = path_env.split(os.pathsep)
  return directory in path_directories

is_posix = not any(platform.win32_ver())

if is_posix:
    ENV_VARIABLE_NAME__LIB="LD_LIBRARY_PATH"
else:
    ENV_VARIABLE_NAME__LIB="LIBPATH"

#os.environ["ROCK_BUILDER_HOME_DIR"] = os.getcwd()
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
os.environ["ROCK_BUILDER_HOME_DIR"] = current_directory
os.environ["ROCK_BUILDER_SRC_DIR"] = os.environ["ROCK_BUILDER_HOME_DIR"] + "/src_projects"
os.environ["ROCK_BUILDER_BUILD_DIR"] = os.environ["ROCK_BUILDER_HOME_DIR"] + "/builddir"

if "ROCM_HOME" not in os.environ:
    rocm_home_root = os.path.abspath(current_directory + "/../build/dist/rocm")
    print("rocm_home_root: " + rocm_home_root)
    if os.path.exists(rocm_home_root):
        os.environ["ROCM_HOME"] = rocm_home_root
        rocm_home_bin = os.path.abspath(rocm_home_root + "/bin")
        rocm_home_lib = os.path.abspath(rocm_home_root + "/lib")
        if os.path.exists(rocm_home_bin):
            if os.path.exists(rocm_home_lib):
                if not is_directory_in_path_env_variable("PATH", rocm_home_bin):
                    print("Adding " + rocm_home_bin + " to PATH")
                    os.environ["PATH"] = rocm_home_bin + os.pathsep + os.environ.get("PATH", "")
                if not is_directory_in_path_env_variable(ENV_VARIABLE_NAME__LIB, rocm_home_lib):
                    print("Adding " + rocm_home_lib + " to " + ENV_VARIABLE_NAME__LIB)
                    os.environ[ENV_VARIABLE_NAME__LIB] = rocm_home_bin + os.pathsep + os.environ.get(ENV_VARIABLE_NAME__LIB, "")
            else:
                print("Error, could not find directory " + rocm_home_lib)
        else:
            print("Error, could not find directory " + rocm_home_bin)
    else:
        print("Error, ROCM_HOME not specified and could not find it from " + rocm_path)
        sys.exit(1)
python_home_dir = os.path.dirname(sys.executable)
if "VIRTUAL_ENV" in os.environ:
    os.environ["ROCK_PYTHON_HOME"] = python_home_dir
else:
    if "ROCK_PYTHON_HOME" in os.environ:
        if not os.path.abspath(python_home_dir) == os.path.abspath(os.environ["ROCK_PYTHON_HOME"]):
            print("Error, virtual python environment is not active and")
            print("PYTHON location is different than ROCK_PYTHON_HOME")
            print("PYTHON location: " + python_home_dir)
            print("ROCK_PYTHON_HOME: " + os.environ["ROCK_PYTHON_HOME"])
            print("If you want use this python location instead of using a virtual python env, define ROCK_PYTHON_HOME:")
            if is_posix:
                print("    export ROCK_PYTHON_HOME=" + python_home_dir)
            else:
                print("    set ROCK_PYTHON_HOME=" + python_home_dir)
            print("Alternatively activate the virtual python environment")
            sys.exit(1)
        else:
            print("Using python from location: " + python_home_dir)
    else:
        print("Error, virtual python environment is not active and ROCK_PYTHON_HOME is not defined")
        print("PYTHON location: " + python_home_dir)
        print("If you want use this python location instead of using a virtual python env, define ROCK_PYTHON_HOME:")
        if is_posix:
            print("    export ROCK_PYTHON_HOME=" + python_home_dir)
        else:
            print("    set ROCK_PYTHON_HOME=" + python_home_dir)
        print("Alternatively activate the virtual python environment")
        sys.exit(1)

print("ROCM_HOME: " + os.environ["ROCM_HOME"])
print("ROCK_PYTHON_HOME: " + os.environ["ROCK_PYTHON_HOME"])
print("ROCK_BUILDER_HOME_DIR: " + os.environ["ROCK_BUILDER_HOME_DIR"])
print("ROCK_BUILDER_SRC_DIR: " + os.environ["ROCK_BUILDER_SRC_DIR"])
print("ROCK_BUILDER_BUILD_DIR: " + os.environ["ROCK_BUILDER_BUILD_DIR"])
print("PATH: " + os.environ["PATH"])
print(ENV_VARIABLE_NAME__LIB + ": " + os.environ[ENV_VARIABLE_NAME__LIB])
time.sleep(1)

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='ROCK Project Builders')

# Add arguments
parser.add_argument('--project', type=str, help='select target for the action. Can be either one project or all projects in core_apps.cfg.', default='all')
parser.add_argument('--checkout',  action='store_true', help='checkout source code for the project', default=False)
parser.add_argument('--clean',  action='store_true', help='clean build files', default=False)
parser.add_argument('--configure',  action='store_true', help='configure project for build', default=False)
parser.add_argument('--build',  action='store_true', help='build project', default=False)
parser.add_argument('--install',  action='store_true', help='install build project', default=False)

# Parse the arguments
args = parser.parse_args()

if ("--checkout" in sys.argv) or ("--clean" in sys.argv) or ("--configure" in sys.argv) or\
   ("--build" in sys.argv) or ("--install" in sys.argv):
    print("checkout/clean/configure/build or install argument specified")
else:
    print("no checkout/clean/configure/build or install argument specified")
    print("assuming all of them are enabled")
    args.checkout=True
    args.configure=True
    args.build=True
    args.install=True

# Access the arguments
print('project:', args.project)
print('checkout:', args.checkout)
print('clean:', args.clean)
print('configure:', args.configure)
print('build:', args.build)
print('install:', args.install)

project_manager = project_builder.RockExternalProjectListManager()
# allow_no_value param says that no value keys are ok
sections = project_manager.sections()
print(sections)
project_list = project_manager.get_external_project_list()
print(project_list)

# checkout all projects
if args.checkout:
    if (args.project == "all"):
        for ii, prj_item in enumerate(project_list):
            print(f"checkout index: {ii}, project: {prj_item}")
            prj_builder = project_manager.get_rock_project_builder(project_list[ii])
            if (prj_builder is None):
                sys.exit(1)
            else:
                prj_builder.printout()
                prj_builder.checkout()
    else:
        prj_builder = project_manager.get_rock_project_builder(args.project)
        if (prj_builder is None):
            sys.exit(1)
        else:
            prj_builder.printout()
            prj_builder.checkout()

if args.clean:
    if (args.project == "all"):
        for ii, prj_item in enumerate(project_list):
            print(f"clean: {ii}, project: {prj_item}")
            prj_builder = project_manager.get_rock_project_builder(project_list[ii])
            if (prj_builder is None):
                sys.exit(1)
            else:
                prj_builder.printout()
                prj_builder.clean()
    else:
        prj_builder = project_manager.get_rock_project_builder(args.project)
        if (prj_builder is None):
            sys.exit(1)
        else:
            prj_builder.printout()
            prj_builder.clean()

if args.configure:
    if (args.project == "all"):
        for ii, prj_item in enumerate(project_list):
            print(f"configure: {ii}, project: {prj_item}")
            prj_builder = project_manager.get_rock_project_builder(project_list[ii])
            if (prj_builder is None):
                sys.exit(1)
            else:
                prj_builder.printout()
                prj_builder.configure()
    else:
        prj_builder = project_manager.get_rock_project_builder(args.project)
        if (prj_builder is None):
            sys.exit(1)
        else:
            prj_builder.printout()
            prj_builder.configure()

if args.build:
    if (args.project == "all"):
        for ii, prj_item in enumerate(project_list):
            print(f"build: {ii}, project: {prj_item}")
            prj_builder = project_manager.get_rock_project_builder(project_list[ii])
            if (prj_builder is None):
                sys.exit(1)
            else:
                prj_builder.printout()
                prj_builder.build()
    else:
        prj_builder = project_manager.get_rock_project_builder(args.project)
        if (prj_builder is None):
            sys.exit(1)
        else:
            prj_builder.printout()
            prj_builder.build()

if args.install:
    if (args.project == "all"):
        for ii, prj_item in enumerate(project_list):
            print(f"install: {ii}, project: {prj_item}")
            prj_builder = project_manager.get_rock_project_builder(project_list[ii])
            if (prj_builder is None):
                sys.exit(1)
            else:
                prj_builder.printout()
                prj_builder.install()
    else:
        prj_builder = project_manager.get_rock_project_builder(args.project)
        if (prj_builder is None):
            sys.exit(1)
        else:
            prj_builder.printout()
            prj_builder.install()
