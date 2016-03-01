# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import re
import codecs

pat = re.compile(u'^[^\u4e00-\u9fa5]')
srcFile=r'D:\PythonProject\AllSentences\AfterFormat--AllSentences.txt'
# srcFile=r'C:\Users\Ack\Desktop\test.txt'

f = codecs.open(srcFile, 'r', 'utf-8')

signHash = {}

lin = f.readline()

while lin:
    # print lin
    res = re.match(pat, lin)
    if res != None:
        print lin
        sign = res.group().strip('\n')
        if signHash.has_key(sign)==False:
            signHash[sign]=1
        else:
            signHash[sign]+=1
    lin = f.readline()
f.close()

for i in signHash:
    print '%s %d ' % (i,signHash[i])
