from dataclasses import dataclass
import subprocess
import os
from PySide6.QtCore import QProcess
from . import cmds
import threading

INSTALL_DONE = threading.Event()

type Blake2BSum = str

def cmd_line(cmd: list[str] | str, capture: bool = True, input: str | None = None, terminal: bool = False) -> subprocess.CompletedProcess:
    if type(cmd) == str:
        cmd = cmd.split(" ")

    result = subprocess.run(cmd, capture_output=capture, text=True, input=input, timeout=60)
        
    if result:
        return result.stdout
    else:
        return None

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

def install(sudo_pswd: str) -> bool:
    INSTALL_DONE = False
    result = cmd_line(f'sudo -S pacman -Sy sbctl --noconfirm --needed',
                      capture=False, input=sudo_pswd+"\n")
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

def is_installed() -> str | None:
    result = cmd_line('pacman -Q sbctl')
    return None if "package 'sbctl' was not found" in result \
            else result
            
def grub() -> None:
    result = cmd_line('sudo grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=cachyos --modules="tpm" --disable-shim-lock')
    