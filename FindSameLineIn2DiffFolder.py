# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import re
import os
import codecs

basePath = os.path.abspath('.')

srcPath= '.\LabeledData'
# srcPath = unicode(srcPath, "utf-8")

resultPath = basePath
# resultPath = unicode(resultPath, "utf-8")

destPath="%s\\quchong" % basePath

def FindSameLineIn2DiffFolder(srcPath, destPath, resultPath):
    duplicateLines = os.path.join(resultPath,'duplicateLinesFrom%sTo%s.txt'% (srcPath.split('\\')[-1],destPath.split('\\')[-1]))
    duplicateLinesFp = codecs.open(duplicateLines,'w','utf-8')
    qaPairsToFileNameHash = {}

    for basePath, dirs, files in os.walk(srcPath):
        for file in files:
            filePath = os.path.join(basePath, file)
            # 每次读三行，若前两行都有内容：第三行为1，第三行为0
            fp = codecs.open(filePath, 'r', 'utf8')
            line1 = fp.readline()
            line2 = fp.readline()
            line3 = fp.readline()

            hashKey = line1
            hashValue = file.split('-')[0]

            while line3:
                qaPairsToFileNameHash[hashKey]=hashValue

                line1 = fp.readline()
                line2 = fp.readline()
                line3 = fp.readline()
                hashKey = line1+line2
            fp.close()

    for basePath, dirs, files in os.walk(destPath):
        for file in files:
            filePath = os.path.join(basePath, file)

            # 每次读三行，若前两行都有内容：第三行为1，第三行为0
            fp = codecs.open(filePath, 'r', 'utf8')
            line1 = fp.readline()
            line2 = fp.readline()
            line3 = fp.readline()

            hashKey = line1
            hashValue = file.split('-')[0]
            hasDuplicateLine = False

            while line3:
                if qaPairsToFileNameHash.has_key(hashKey)==True:
                    hasDuplicateLine = True
                    print '%s<--%s--:--%s' % (qaPairsToFileNameHash[hashKey],hashValue,line1)
                    duplicateLinesFp.write('%s<--%s--:--%s' % (qaPairsToFileNameHash[hashKey],hashValue,line1))
                line1 = fp.readline()
                line2 = fp.readline()
                line3 = fp.readline()
                hashKey = line1+line2
                # print line1,line2,line3
            fp.close()
            if hasDuplicateLine:
                print '\n'
                duplicateLinesFp.write('\n')
    duplicateLinesFp.close()

if __name__ == '__main__':
    FindSameLineIn2DiffFolder(srcPath,destPath,resultPath)