from dataclasses import dataclass
import os
from PySide6.QtCore import QProcess, QIODeviceBase
from PySide6.QtWidgets import QWidget
from types import FunctionType
from . import cmds

type B2Sum = str
type SudoPassword = str

PROCESSOR = QProcess()
PROCESSOR.open(QIODeviceBase.OpenModeFlag.ReadWrite)

SUDO = 'sudo'

async def cmdline(cmd: list[str], *, pswd: str | None = None) -> str:
    cmdStr = " ".join(cmd)
    print(f"Executing: '{cmdStr}'")
    
    if pswd and cmd[0] == SUDO:
        cmd.insert(1, '-S')
    PROCESSOR.finished.connect(lambda: print(f"Finished: {cmdStr}"))
    
    try:
        PROCESSOR.start(cmd[0], cmd[1:])
        if PROCESSOR.waitForStarted(3000) and cmd[0] == SUDO and pswd:
            pswd += "\n"
            PROCESSOR.write(pswd.encode("utf-8"))
        
        if PROCESSOR.waitForStarted() and PROCESSOR.waitForFinished():
            output = PROCESSOR.readAllStandardOutput().data().decode().strip()
            return output
    except Exception as err:
        return err
        
class _sbctl():
    def __init__(self):
        pass
    
    def cmdline(cmd: list[str]) -> str:
        pass
    
    def b2sum(self) -> B2Sum:
        pass
    
    def install(self) -> bool:
        pass
    
    def is_installed(self) -> bool:
        pass
    
    def create_keys(self) -> bool:
        pass
    
    def enroll_keys(self) -> bool:
        pass
    
    def status(self) -> str:
        self.process.start(cmds.status)
    
    def link_terminal(self, *, stdout: FunctionType, stderr: FunctionType) -> bool:
        '''
        This will allow you to print the stdout and stderr to your internal terminal.
        
        Arguments:
            stdout - The callable to link to QProcess for stdout
            stderr - The callable to link to QProcess for stderr
        '''
        linked = False
        if not callable(stdout):
            print("stdout method is not callable!")
        elif not callable(stderr):
            print('stderr method is not callable!')
        else:
            self.process.readyReadStandardOutput.connect(stdout)
            self.process.readyReadStandardError.connect(stderr)
            linked = True
        
        return linked

    def end_process(self) -> None:
        pass

_SBCTL = _sbctl()

async def b2sum() -> B2Sum:
    pass

async def install(sudo: SudoPassword) -> bool:
    result = await cmdline(['sudo', 'pacman', '-Sy', 'sbctl', '--noconfirm'], pswd=sudo)

async def is_installed() -> bool:
    print("Checking sbctl installation...")
    return False

async def create_keys() -> bool:
    pass

async def enroll_keys() -> bool:
    pass

async def status() -> str:
    status = await cmdline(['sudo', 'sbctl', 'status'])

def link_terminal(*, stdout: FunctionType, stderr: FunctionType) -> bool:
    '''
    This will allow you to print the stdout and stderr to your internal terminal.

    Arguments:
        stdout - The callable to link to QProcess for stdout
        stderr - The callable to link to QProcess for stderr
    '''
    linked = False
    if not callable(stdout):
        print("stdout method is not callable!")
    elif not callable(stderr):
        print('stderr method is not callable!')
    else:
        PROCESSOR.readyReadStandardOutput.connect(stdout)
        PROCESSOR.readyReadStandardError.connect(stderr)
        linked = True
        print("Terminal linked.")
        
    return linked
    
def set_pyside6():
    IS_PYSIDE6 = True