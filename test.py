# -*- coding:utf-8 -*-

import re

result = re.match('\[\]\Z', '[你好]')
if result:
    print result.group();
else:
    print 'No find\n'
    
