

str2 = '''\033[0;35m很豪华\033[0m'''

print(repr(str2))

import re

pattern = re.compile('\\033\[.+?m')

print(repr(pattern.sub('',str2)))