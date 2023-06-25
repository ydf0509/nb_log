import time

from colorama import just_fix_windows_console, Fore
# from termcolor import colored
#
# # use Colorama to make Termcolor work on Windows too
# # just_fix_windows_console()
#
# # then use Termcolor for all colored text output
# print(colored('Hello, World!', 'green', 'on_red'))





from colorama import init
init(autoreset=True)
print(Fore.RED + 'some red text')
print('automatically back to default color again')





time.sleep(110000)