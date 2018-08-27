#!/usr/bin/env python3
"""Runs precommit checks on the repository."""
import argparse
import pathlib
import subprocess
import sys


def main() -> int:
    """"
    Main routine
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--overwrite",
        help="Overwrites the unformatted source files with the well-formatted code in place. "
        "If not set, an exception is raised if any of the files do not conform to the style guide.",
        action='store_true')

    args = parser.parse_args()

    overwrite = bool(args.overwrite)

    repo_root = pathlib.Path(__file__).parent

    print("YAPF'ing...")
    if overwrite:
        subprocess.check_call(
            ["yapf", "--in-place", "--style=style.yapf", "--recursive", "tests", "lexery", "setup.py", "precommit.py"],
            cwd=repo_root.as_posix())
    else:
        subprocess.check_call(
            ["yapf", "--diff", "--style=style.yapf", "--recursive", "tests", "lexery", "setup.py", "precommit.py"],
            cwd=repo_root.as_posix())

    print("Mypy'ing...")
    subprocess.check_call(["mypy", "lexery", "tests"], cwd=repo_root.as_posix())

    print("Pylint'ing...")
    subprocess.check_call(["pylint", "--rcfile=pylint.rc", "tests", "lexery"], cwd=repo_root.as_posix())

    print("Pydocstyle'ing...")
    subprocess.check_call(["pydocstyle", "lexery"], cwd=repo_root.as_posix())

    print("Doctest'ing ...")
    subprocess.check_call(['python', '-m', 'doctest', 'README.rst'])
    subprocess.check_call(
        ['python', '-m', 'doctest'] + [pth.as_posix() for pth in pathlib.Path("lexery").glob("**/*.py")])

    print("Testing...")
    subprocess.check_call(
        ["coverage", "run", "--source", "lexery", "-m", "unittest", "discover", "tests"], cwd=repo_root.as_posix())

    subprocess.check_call(["coverage", "report"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
