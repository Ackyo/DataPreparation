# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import re
import os
import codecs

srcPath = u'D:\\待标注对话组'

# 统计根目录下个个文件的对话数以及总对话数
def CountQAPairs(srcPath):
    Total = 0
    for file in os.listdir(srcPath):
        count = 0
        filePath = os.path.join(srcPath, file)
        print filePath
        if os.path.isfile(filePath):
            # 每次读三行，若前两行都有内容：第三行为1，第三行为0
            fp = codecs.open(filePath, 'r', 'utf8')
            line1 = fp.readline()
            line2 = fp.readline()
            line3 = fp.readline()
            while line3:
                count += 1
                line1 = fp.readline()
                line2 = fp.readline()
                line3 = fp.readline()
            print '---%s : %d pairs\n' % (file, count)
            Total += count
    print 'Total: %d pairs\n' % Total

if __name__ == '__main__':
    CountQAPairs(srcPath)
