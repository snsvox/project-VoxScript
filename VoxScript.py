import math
from altair import condition
from colorama import Fore,Back,Style,init
import sys
import signal
import os
import webbrowser
import threading
import time
import pyfiglet
import requests

voxscript = pyfiglet.Figlet('standard')

t = time.localtime()

class CommandError(Exception):
    pass
class TerminalError(Exception):
    pass
class RepeatError(Exception):
    pass
class LoopError(Exception):
    pass

init(autoreset=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()

print(Fore.CYAN + voxscript.renderText("Ran in VoxScript"))
print(Fore.GREEN + f">>> VoxScript Initialization Complete, to remove this watermark completely, open VoxScript.py, no need to pay")
print(Fore.YELLOW + ">>> File Ran in:", os.getcwdb(), '\n')

def exit_error(error,type_of_error,reason):
    if error == 1:
        type = type_of_error
        reason_of_error = reason
        raise type(reason_of_error)
    elif error == 0:
        pass
    else:
        raise SyntaxError("Invaild type of trigger. Did you mean 0 (0 does not trigger) or 1 (1 triggers the error as long as there is the reason why)")


log1 = lambda *args: print(*args)

def exit(trigger):
    if trigger == 0:
        pass
    elif trigger == 1:
        print("Process or program ended with exit code 0")
        sys.exit(0)
    else:
        raise SyntaxError("Invaild type of trigger. Did you mean 0 (0 does not trigger it) or 1 (triggers it), Process or program ended with exit code 1")

def console_json(*args):
    print(args)

#PLEASE NOTE! all commands the must have a "/" in it, commands are down from the definition, if the command does not have text, leave the text part AS "1"
def console_command(command,text):
    if not command.startswith('/'):
        raise SyntaxError("Commands has to start with'/'")
    if text == "command.cancel":
        pass
    if command == '/write_down':
        console_write(text)
    if command == '/end':
        sys.exit(0)
    if command == '/shutdown_terminal':
        print(Fore.YELLOW + "Kill the Terminal? This action may not do anything but kill the terminal!",Style.BRIGHT + "Y/N")
        choice = input()
        if choice == "Y" or "y":
            os.system(f"taskkill /F /PID {os.getppid() if os.name == 'nt' else os.kill(os.getppid(), signal.SIGKILL)
}")
        else:
            pass
    if command == '/command.cancel':
        pass

    if command == '/open_website':
        webbrowser.open(text)

    if command == '/clear':
        clear()

    if command == '/exit':
        exit(int(text))

    if command == '/error':
        exit_error(int(text), CommandError, "User triggered error")

    if command == '/terminal_error':
        exit_error(int(text), TerminalError, "User triggered terminal error")

    if command == '/json':
        console_json(text)

    if command == '/help':
        console_write("Available commands: /write_down, /end, /shutdown_terminal, /command.cancel, /open_website, /clear, /exit, /error, /terminal_error, /json, /help")
        console_write("For the definition of all commands, type /help_advanced")
    
    if command == '/help_advanced':
        console_write("/write_down: Given text will be written to the console")
        console_write("/end: Ends the program with exit code 0")
        console_write("/shutdown_terminal: Kills the terminal (after confirmation)")
        console_write("/command.cancel: Cancels the current command")
        console_write("/open_website: Opens the disired website into your browser")
        console_write("/clear: Clears the console")
        console_write("/exit: Exits the program with the given exit code")
        console_write("/error: Triggers an error with the given exit code")
        console_write("/terminal_error: Triggers a terminal error with the given exit code")
        console_write("/json: Outputs the given text in JSON line")
        console_write("/help_advanced: Displays this advanced help message")
        console_write("/help: Displays all available commands")

i = True
o = False

trigger = 0

def loop_stop():
    global trigger
    trigger = 1

def loop(*f, delay=0):
    while True:
        if trigger == 1:
            break
        else:
            pass
        for func in f:
            try:
                func()
                time.sleep(delay)
            except Exception as e:
                raise LoopError(f"Nonetype is not callable, maybe you forgot to add lambda function")

def repeat(number_of_times,*args,delay=0):
    error = args
    for _ in range(number_of_times):
        for func in args:
            try:
                func()
                time.sleep(delay)
            except Exception as e:
                raise RepeatError(f"Nonetype is not callable, maybe you forgot to add lambda function to each argument or pos arg")

def wait(delay=0):
    time.sleep(delay)

def delay(time):
    time.sleep(time)

def debug_start():
    console_write(">>>DEBUG STARTED - Errors will be listed in the console or at any point in the developer app")
    console_write(">>>REMINDER: VoxScript is ran purely in python, any errors are handled by the Python interpreter")
    breakpoint()

def py_function(*args):
    args

def var(name,value=0):
    globals()[name] = value

class ReplaceError(Exception):
    pass

def replace(var,new_value):
    if var not in globals():
        raise NameError(f"Variable '{var}' is undefined. Did you forgot to define {var}?")
    try:
        globals()[var] = new_value
    except Exception as e:
        raise ReplaceError(f"Failed to replace variable '{var}' with new value '{new_value}': {e}")

def console_write(*args):
    try:
        log1(*args)
    except NameError as e:
        print(f"{args} is not defined! Error: {e}")

def verify_var(name):
    if name not in globals():
        console_write(f"Variable: '{name}' is not defined!")
    else:
        console_write(f"Variable: '{name}' is defined!, Value: {globals()[name]}")

def calc(args,write=False):
    if not any(op in args for op in ['-', '+', '*', '/', '%', '**', '//']) or 'math' in args:
        raise SyntaxError(f"'calc' function does not calculate {args}. If this is a mistake (like sin() in math), then use the function since math is imported instead")
    else:
        try:
            result = eval(args)
            if write:
                float(console_write(result))
            return result
        except Exception as e:
            console_write(f"Error calculating expression '{args}': {e}")

def sin(x):
    return math.sin(x)

def cos(x):
    return math.cos(x)

def tan(x):
    return math.tan(x)

def exp(x):
    return math.exp(x)

def sqrt(x):
    return math.sqrt(x)


def os_check(write=False):
    if write:
        console_write(f"Operating System: {'linux' if os.name == 'posix' else 'windows' if os.name == 'nt' else 'undefined'}")
    elif not write:
        return os.name
    else:
        raise NameError("func: os_check is called with an invalid argument, did you mean True or False?")

log2 = lambda *args: input(f"{args[0]}")

def prompt_ask(*args,arrow=False,SPACE=False):
    if not arrow:
        return log2(f"{args[0]} " if SPACE else f"{args[0]}")
    else:
        log(f"{args[0]}")
        return input(">>> ")

logger = ""
    
def log(*args):
    global logger
    logger += f"{args[0]} \n"

def log_clear(start=False):
    global logger
    if start:
        logger = ""
    else:
        pass

class LogError(Exception):
    pass

def log_save(filename,status=False):
    if not status:
        pass
    else:
        console_write(f"Log saving as {filename}")
    global logger
    try:
        with open(filename, 'w') as f:
            f.write(logger)

    except Exception as e:
        raise LogError(f"Failed to save log: '{filename}'. Error: {e}")

def exit():
    raise SystemExit

def terminal_command(command):
    if not command.startswith('/'):
        raise CommandError(f"Commands start with '/' not {command.startswith('/' if not command.startswith('/') else command)}")
    else:
        command = command.removeprefix('/')
        eval(command)


class FileError(Exception):
    pass

class file:
    def __init__(self,name):
        self.name = name

    def overwrite(filename,*args):
        os.remove(filename)
        with open(filename,'w') as f:
            f.write(args)

    def file_read(filename,write=False):
        try:
            with open(filename, 'r') as f:
                content = f.read()
                if write:
                    console_write(content)
                return content
        except Exception as e:
            raise LogError(f"Failed to read log: '{filename}'. Error: {e}")

    def delete(filename):
        os.remove(filename)

    def make(filename,*args):
        with open(filename,'w') as f:
            f.write(*args)

class ComputerError(Exception):
    pass

class computer:
    def __init__(self,name):
        self.name = name

    def scannow():
        if os.name == 'nt':
            import ctypes
            globals()[my_command] = 'sfc /scannow'
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", my_commands, None, 1)
        else:
            raise ComputerError(f"Your OS is linux and sfc can only be ran in windows")

    #not much here since idk give me ideas

class code:
    def __init__(self,name):
        self.name = name

    def call(variable):
        if variable in globals():
            return f'Variable: "{variable}" found as value: {globals()[variable]}'
        else:
            raise NameError(f'Variable: "{variable}" is not defined!')

class py:
    def __init__(self,name):
        self.name = name

    def run(filename):
                with open(filename,'rb') as f:
                    content = f.read()
                    exec(content)
