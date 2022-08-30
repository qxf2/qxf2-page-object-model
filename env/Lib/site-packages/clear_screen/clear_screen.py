from subprocess import call
from sys import platform


def clear():
    if platform not in ('win32', 'cygwin'):
        command = 'clear'
    else:
        command = 'cls'
    call(command, shell=True)
