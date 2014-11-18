import pdb
from dbnav import navigator

navigator.run(['', '-l', 'debug', 'dbnav.sqlite/user?id='])
navigator.run(['', '-l', 'debug', 'dbnav.sqlite/user/?id=66'])
