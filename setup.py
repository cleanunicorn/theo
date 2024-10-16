from setuptools import setup, find_packages
from theo.version import __version__
from setuptools.command.install import install
import sys
import os


def read_file(fname):
    """
    return file contents
    :param fname: path relative to setup.py
    :return: file contents
    """
    with open(os.path.join(os.path.dirname(__file__), fname), "r") as fd:
        return fd.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""

    description = "verify that the git tag matches our version"

    def run(self):
        tag = os.getenv("CIRCLE_TAG")

        if tag != __version__:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, __version__
            )
            sys.exit(info)


setup(
    name="theo",
    version=__version__,
    license="MIT",
    author="Daniel Luca",
    author_email="daniel.luca@consensys.net",
    long_description=read_file("Readme.md") if os.path.isfile("Readme.md") else "",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=read_file("requirements.txt").split("\n"),
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["theo=theo.interfaces.cli:main"]},
    cmdclass={"verify": VerifyVersionCommand},
    url="https://github.com/cleanunicorn/theo",
)
