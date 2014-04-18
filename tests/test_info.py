#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket
import getpass

import pytest

from pyscaffold import info
from pyscaffold import runner
from .fixtures import git_mock, nogit_mock, tmpdir

__author__ = "Florian Wilhelm"
__copyright__ = "Blue Yonder"
__license__ = "new BSD"


def test_username_with_git(git_mock):
    username = info.username()
    assert isinstance(username, str)
    assert len(username) > 0


def test_username_with_no_git(nogit_mock):
    username = info.username()
    assert isinstance(username, str)
    assert getpass.getuser() == username


def test_email_with_git(git_mock):
    email = info.email()
    assert "@" in email


def test_email_with_nogit(nogit_mock):
    email = info.email()
    assert socket.gethostname() == email.split("@")[1]


def test_git_is_installed(git_mock):
    assert info.git_is_installed()


def test_git_is_not_installed(nogit_mock):
    assert not info.git_is_installed()


def test_project_raises():
    args = type("Namespace", (object,), {"project": "non_existant"})
    with pytest.raises(RuntimeError):
        info.project(args)


def test_project_without_args(tmpdir):
    old_args = ["my_project", "-u", "http://www.blue-yonder.com/",
                "-d", "my description"]
    runner.main(old_args)
    args = ["my_project"]
    args = runner.parse_args(args)
    new_args = info.project(args)
    assert new_args.url == "http://www.blue-yonder.com/"
    assert new_args.package == "my_project"
    assert new_args.license == "new BSD"
    assert new_args.description == "my description"


def test_project_with_args(tmpdir):
    old_args = ["my_project", "-u", "http://www.blue-yonder.com/",
                "-d", "my description"]
    runner.main(old_args)
    args = ["my_project", "-u", "http://www.google.com/",
            "-d", "other description", "-l", "new-bsd"]
    args = runner.parse_args(args)
    new_args = info.project(args)
    assert new_args.url == "http://www.google.com/"
    assert new_args.package == "my_project"
    assert new_args.license == "new BSD"
    assert new_args.description == "other description"


def test_project_with_no_setup(tmpdir):
    os.mkdir("my_project")
    args = ["my_project"]
    args = runner.parse_args(args)
    with pytest.raises(RuntimeError):
        info.project(args)


def test_project_with_wrong_setup(tmpdir):
    os.mkdir("my_project")
    open("my_project/setup.py", 'a').close()
    args = ["my_project"]
    args = runner.parse_args(args)
    with pytest.raises(RuntimeError):
        info.project(args)
