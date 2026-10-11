from dataclasses import dataclass
import os
from PySide6.QtCore import QProcess, QObject, Signal
from PySide6.QtWidgets import QWidget
from types import FunctionType
from . import cmds
from dataclasses import dataclass

type B2Sum = str
type SudoPassword = str

PROCESSOR = QProcess()

STDOUT: FunctionType = None
STDERR: FunctionType = None

SUDO = 'sudo'

PROCESSOR = QProcess()
LAST_VAL = None

class _TerminalSignal(QObject):
    StandardOut = Signal(str)
    StandardError = Signal(str)
    Print = Signal(str)


class Terminal:
    Output = _TerminalSignal()
    
    @staticmethod
    def readAllStandardOutput() -> str:
        return PROCESSOR.readAllStandardOutput().data().decode().strip()
    
    @staticmethod
    def readAllStandardError() -> str:
        return PROCESSOR.readAllStandardError().data().decode().strip()
    
def show_output() -> None:
    Terminal.Output.StandardOut.emit(Terminal.readAllStandardOutput())
    Terminal.Output.StandardError.emit(Terminal.readAllStandardError())

def cmdline(cmd: list[str], *, pswd: str | None = None, hold_output: bool = False) -> str:
    cmdStr = " ".join(cmd)
    
    while PROCESSOR.state() == QProcess.ProcessState.Running:
        pass
    
    Terminal.Output.Print.emit(f"Executing: '{cmdStr}'")
    if not hold_output:
        PROCESSOR.readyReadStandardOutput.connect(show_output)
    
    try:
        PROCESSOR.start(cmd[0], cmd[1:])
        if pswd and PROCESSOR.waitForStarted(1000):
            pswd += "\n"
            PROCESSOR.write(pswd.encode())
            PROCESSOR.closeWriteChannel()
        
        if hold_output:
            if PROCESSOR.waitForFinished():
                output = Terminal.readAllStandardOutput()
                errs = Terminal.readAllStandardError()
                Terminal.Output.StandardOut.emit(output)
                Terminal.Output.StandardError.emit(errs)
                Terminal.Output.Print.emit(f"Finished: '{cmdStr}'")
                if output:
                    return output
                if errs:
                    return errs
        else:
            return None
        
    except Exception as err:
        print(f"ERROR: {err}")


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

def b2sum() -> B2Sum:
    pass

def install(sudo: SudoPassword) -> bool:
    result = cmdline(
        ['sudo', 'pacman', '-Sy', 'sbctl', '--noconfirm' ,'--needed'],
        pswd=sudo
    )
    return is_installed()

def is_installed() -> bool:
    result = cmdline(['pacman', '-Q', 'sbctl'], hold_output=True)
    if result == "error: package 'sbctl' was not found":
        return False
    else:
        return True

def create_keys() -> bool:
    pass

def enroll_keys() -> bool:
    pass

def status() -> str:
    if Terminal.Linked:
        Terminal.Print("Getting sbctl status...")
    status = cmdline(['sbctl', 'status'])
    return status

def link_terminal(*, print: FunctionType, proc_out: FunctionType, proc_err: FunctionType) -> bool:
    '''
    This will allow you to print the stdout and stderr to your internal terminal.

    Arguments:
        stdout - The callable to link to QProcess for stdout
        stderr - The callable to link to QProcess for stderr
    '''
    if not callable(proc_out):
        print("stdout method is not callable!")
    elif not callable(proc_err):
        print('stderr method is not callable!')
    else:
        Terminal.Print = print
        Terminal.ProcOut = proc_out
        Terminal.ProcErr = proc_err
        Terminal.Linked = True
        
    return Terminal.Linked
    
def set_pyside6():
    IS_PYSIDE6 = True