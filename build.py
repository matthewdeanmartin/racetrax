# coding=utf-8
"""
mini-first-impressions review:
- good build dependencies
- easy to call python things
- cumbersome to call things normally done in bash.
- if I actually used it, I would probably have 50% of code in tiny bash scripts, 1 per task.
- loops, if-blocks, etc less painful than bash.
- no easy way to redirect output of script to file
- no way to use this to set up venvs, nor to do deployment (needs venv to run this!)

Loading packages is often surprsing.
"""
# import os
# os.environ["PYTHONPATH"] = "."
#
# from pynt_extras import *

from pyntcontrib import *
from semantic_version import Version

PROJECT_NAME = "racetrax"
PYTHON = "python3.6"
IS_DJANGO = False

# coding=utf-8
"""
Pynt was missing some things I desperately wanted.
"""
import os

from checksumdir import dirhash

CURRENT_HASH = None


# bash to find what has change recently
# find src/ -type f -print0 | xargs -0 stat -f "%m %N" | sort -rn | head -10 | cut -f2- -d" "
class BuildState(object):
    def __init__(self, what, where):
        self.what = what
        self.where = where
        if not os.path.exists(".build_state"):
            os.makedirs(".build_state")
        self.state_file_name = ".build_state/last_change_{0}.txt".format(what)

    def oh_never_mind(self):
        """
        If a task fails, we don't care if it didn't change since last, re-run,
        :return:
        """
        os.remove(self.state_file_name)

    def has_source_code_tree_changed(self):
        """
        If a task succeeds & is re-run and didn't change, we might not
        want to re-run it if it depends *only* on source code
        :return:
        """
        global CURRENT_HASH
        directory = self.where

        if CURRENT_HASH is None:
            CURRENT_HASH = dirhash(directory, 'md5', excluded_files="*.pyc")

        if os.path.isfile(self.state_file_name):
            with open(self.state_file_name, "r+") as file:
                last_hash = file.read()
                if last_hash != CURRENT_HASH:
                    file.seek(0)
                    file.write(CURRENT_HASH)
                    file.truncate()
                    return True
        else:
            with open(self.state_file_name, "w") as file:
                file.write(CURRENT_HASH)
                return True
        return False


def oh_never_mind(what):
    state = BuildState(what, PROJECT_NAME)
    state.oh_never_mind()


def has_source_code_tree_changed(what):
    state = BuildState(what, PROJECT_NAME)
    return state.has_source_code_tree_changed()


import functools


def skip_if_no_change(name):
    # https://stackoverflow.com/questions/5929107/decorators-with-parameters
    def real_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not has_source_code_tree_changed(name):
                print("Nothing changed, won't re-" + name)
                return
            try:
                return func(*args, **kwargs)
            except:
                oh_never_mind(name)
                raise

        return wrapper

    return real_decorator


def execute_with_environment(command, env):
    nose_process = subprocess.Popen(command.split(" "), env=env)
    nose_process.communicate()  # wait


import subprocess


def execute_get_text(command):
    try:
        completed = subprocess.run(
            command,
            check=True,
            shell=True,
            stdout=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as err:
        raise
    else:
        # print('returncode:', completed.returncode)
        # print('Have {} bytes in stdout: {!r}'.format(
        #     len(completed.stdout),
        #     completed.stdout.decode('utf-8'))
        # )
        return completed.stdout.decode('utf-8')


@task()
# @skip_if_no_change("bumpversion")
def bumpversion():
    """
    Fails if git isn't committed.
    :return:
    """
    # hide until fixed.
    return
    x = execute_get_text(" ".join(["python", "-c", '"import keno;print(keno.__version__)"']))
    print(x)
    current_version = Version(x)
    # new_version = Version("{0}{1}{2}".format(current_version.major, current_version.minor, current_version.build +1))
    # bumpversion --new-version 2.0.2 build --no-tag  --no-commit
    execute("bumpversion", "--current-version", str(current_version), "build", "--tag", "--no-commit")


@task()
@skip_if_no_change("clean")
def clean():
    for folder in ["build", "dist", PROJECT_NAME + ".egg-info"]:
        execute("rm", "-rf", folder)

    try:
        execute("rm", "lint.txt")
    except:
        pass


@task(clean)
@skip_if_no_change("compile")
def compile():
    execute("python", "-m", "compileall", PROJECT_NAME)


@task(compile)
@skip_if_no_change("lint")
def lint():
    # sort of redundant to above...
    #
    execute("prospector",
            *("{0} --profile {0}_style --pylint-config-file=pylintrc.ini --profile-path=.prospector"
              .format(PROJECT_NAME)
              .split(" ")))

    command = "pylint --rcfile=pylintrc.ini {0}".format(PROJECT_NAME)
    bash_process = subprocess.Popen(command.split(" "),
                                    #shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE
                                    )
    out, err = bash_process.communicate()  # wait
    print("----")

    with open("lint.txt", "w+") as lint_file:
        lint_file.write(out.decode())

    num_lines = sum(1 for line in open('lint.txt'))
    if num_lines > 100:
        raise TypeError("Too many lines of lint : {0}".format(num_lines))


@task(lint)
@skip_if_no_change("nose_tests")
def nose_tests():
    # if these were integration tests with say, API calls, we might not want to skip
    execute(PYTHON, "-m", "nose", PROJECT_NAME)


@task(nose_tests)
@skip_if_no_change("coverage")
def coverage():
    # if these were integration tests with say, API calls, we might not want to skip
    execute("py.test", *("{0} --cov={0} --cov-report html:coverage --verbose"
                         .format(PROJECT_NAME)
                         .split(" ")))


@task(nose_tests)
@skip_if_no_change("docs")
def docs():
    with safe_cd("docs"):
        execute("make", "html")


@task()
@skip_if_no_change("pip_check")
def pip_check():
    execute("pip", "check")
    execute("safety", "check")
    execute("safety", "check", "-r", "requirements_dev.txt")


@task(docs, nose_tests, pip_check, compile, lint)
@skip_if_no_change("package")
def package():
    execute("pandoc", *("--from=markdown --to=rst --output=README.rst README.md".split(" ")))
    execute(PYTHON, "setup.py", "sdist", "--formats=gztar,zip")

@task()
@skip_if_no_change("type_checking")
def type_checking():

    command = "mypy {0} --ignore-missing-imports --strict".format(PROJECT_NAME)
    bash_process = subprocess.Popen(command.split(" "),
                                    #shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE
                                    )
    out, err = bash_process.communicate()  # wait
    print("----")

    with open("mypy_errors.txt", "w+") as lint_file:
        lint_file.write(out.decode())

    num_lines = sum(1 for line in open('mypy_errors.txt'))
    if num_lines > 10:
        raise TypeError("Too many lines of mypy : {0}".format(num_lines))

@task()
def echo(*args, **kwargs):
    print(args)
    print(kwargs)


# Default task (if specified) is run when no task is specified in the command line
# make sure you define the variable __DEFAULT__ after the task is defined
# A good convention is to define it at the end of the module
# __DEFAULT__ is an optional member

__DEFAULT__ = echo
