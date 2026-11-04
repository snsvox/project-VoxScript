import math
from colorama import Fore,Back,Style,init
import sys
import signal
import os
import webbrowser
import threading
import time

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

def exit_error(error,type_of_error,reason):
    if error == 1:
        type = type_of_error
        reason_of_error = reason
        raise type(reason_of_error)
    elif error == 0:
        pass
    else:
        raise SyntaxError("Invaild type of trigger. Did you mean 0 (0 does not trigger) or 1 (1 triggers the error as long as there is the reason why)")


log = lambda *args: print(*args)

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

def i():
    pass

def o():
    pass

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

def var(name,value):
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

def define(name,*args):
    def name():
        for func in args:
            func()
    globals()[name] = name

def console_write(*args):
    log(*args)
