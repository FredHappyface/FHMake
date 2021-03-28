"""Utils used by the rest of fhutils."""

from __future__ import annotations

import platform
import subprocess
import typing
from pathlib import Path

import tomlkit
import tomlkit.items
from tomlkit import toml_document

PY = "py" if platform.system() == "Windows" else "python3"
ANSI = {
	"B": "\033[01m",
	"CLR": "\033[00m",
	"U": "\033[04m",
	"CB": "\033[36m",
	"CG": "\033[32m",
	"CY": "\033[33m",
	"CR": "\033[31m",
	"CODE": "\033[100m\033[93m",
}


def _getPyproject() -> typing.Any:
	"""Get the pyproject data."""
	with open("pyproject.toml", encoding="utf=8") as pyproject:
		return tomlkit.parse(pyproject.read())


def _setPyproject(toml: toml_document.TOMLDocument):
	"""Write the pyproject data back to file."""
	with open("pyproject.toml", "w", encoding="utf=8") as pyproject:
		pyproject.write(tomlkit.dumps(toml))


def _doSysExec(command: str) -> tuple[int, str]:
	"""Execute a command and check for errors.

	Args:
		command (str): commands as a string

	Raises:
		RuntimeWarning: throw a warning shoANSI['U']d there be a non exit code

	Returns:
		tuple[int, str]: return code + stdout
	"""
	with subprocess.Popen(
		command,
		shell=True,
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT,
		encoding="utf-8",
		errors="ignore",
	) as process:
		out = process.communicate()[0]
		exitCode = process.returncode
	return exitCode, out


NAME = str(_getPyproject()["tool"]["poetry"]["name"])
