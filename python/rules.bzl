"""Rules for python envs and testing"""
load("@aspect_rules_py//py:defs.bzl", "py_test")
load("@rules_python//python:defs.bzl", _py_binary = "py_binary", _py_library = "py_library")
load("@rules_pyvenv//:venv.bzl", _py_venv = "py_venv")
load("//rules/lint:linters.bzl", "ruff_test")

def name_to_target(name):
    return ":" + name

def append_dot_name(name, dot_name):
    return name + dot_name

def py_library(name, srcs, **kwargs):
    _py_library(
        name = name,
        srcs = srcs,
        **kwargs
    )
    ruff_test(name = append_dot_name(name, ".lint"), srcs = [name_to_target(name)])

def py_binary(name, srcs, **kwargs):
    _py_binary(name = name, srcs = srcs, **kwargs)
    ruff_test(name = append_dot_name(name, ".rufflint"), srcs = [name_to_target(name)])


def pytest_test(name, srcs, deps, **kwargs):
    srcs.append("//python:__test__")

    if "@pip//pytest:pkg" not in deps:
        deps.append("@pip//pytest:pkg")

    py_test(name = name, srcs = srcs, deps = deps, **kwargs)

def py_venv(name, deps, **kwargs):
    _py_venv(name = name, deps = deps, **kwargs)
