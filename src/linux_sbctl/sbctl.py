from dataclasses import dataclass
import subprocess
import os
from PySide6.QtCore import QProcess
from . import cmds

type Blake2BSum = str

def cmd_line(cmd: list[str]) -> subprocess.CompletedProcess:
    subprocess.run(cmd, capture_output=True, text=True)

@dataclass
class cnsts:
    SETUP_ENABLED = "Setup Mode:     ✗ Enabled"
    DISABLED_SETUP="Setup Mode:     ✗ Disabled"
    COMPLETE_SETUP="Setup Mode:     ✓ Disabled "
    SECUREBOOT_ENABLED = "Secure Boot:    ✓ Enabled"
    NOT_INSTALLED = 'not_installed'

@dataclass
class statuses:
    SETUP_ENABLED = "Setup Mode:     ✗ Enabled"
    DISABLED_SETUP="Setup Mode:     ✗ Disabled"
    COMPLETE_SETUP="Setup Mode:     ✓ Disabled "
    SECUREBOOT_ENABLED = "Secure Boot:    ✓ Enabled"
    NOT_INSTALLED = 'not_installed'

class Processor(QProcess):
    def __init__(self, parent):
        super().__init__(parent=parent)


PROCESSOR = Processor()

# TODO: setup for Qt and regular use
def install() -> bool:
    result = cmd_line(cmds.install)
    return is_installed()
    
def create_keys() -> bool:
    pass

def enroll_kets() -> bool:
    pass

def hash() -> Blake2BSum:
    pass

def hash_wallpaper() -> str:
    pass

def get_progress() -> int:
    pass

def is_installed() -> bool:
    cmd = ['pacman', '-Q', 'sbctl']
    result = cmd_line(cmd).stdout
    return False if "error: package 'sbctl' was not found" in result \
            else True
    