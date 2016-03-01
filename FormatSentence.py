# coding=utf-8
import sys
import codecs
import os
import re

reload(sys)
sys.setdefaultencoding('utf8')

srcData = "D:\PythonProject\AllSentences\AllSentences.txt"
srcData = unicode(srcData, "utf-8")

resultFile = 'AfterFormat--AllSentences.txt'
resultPath = "D:\PythonProject\AllSentences"


def RemoveDuplicateLines(srcData, resultFile):
    content2LineNumHash = {}
    fp = codecs.open(srcData, 'r', 'utf8')
    resultFileFp = codecs.open(os.path.join(resultPath, resultFile), 'w', 'utf-8')

    curLine = fp.readline()
    lineNum = 1
    removeDuplicatesFp = codecs.open(os.path.join(resultPath, 'Duplicates.log'), 'w', 'utf-8')
    duplicateLines = 0
    while curLine:
        if content2LineNumHash.has_key(curLine) == False:
            content2LineNumHash[curLine] = lineNum
            resultFileFp.write(curLine)
        else:
            print 'Duplicate: Line %d <-- Line %d : %s' % (content2LineNumHash[curLine], lineNum, curLine)
            removeDuplicatesFp.write('Line %d <-- Line %d : %s' % (content2LineNumHash[curLine], lineNum, curLine))
            duplicateLines += 1
        curLine = fp.readline()
        lineNum += 1
    print '-------------Total Lines: %d -- Duplicate Lines: %d -- Repetitive Rate %.2f%% -- Remain %d Lines----------------\n' % (
    lineNum, duplicateLines, 100.0 * duplicateLines / lineNum, lineNum - duplicateLines)
    fp.close()
    removeDuplicatesFp.close()
    resultFileFp.close()


def StripPrelude(srcStr):
    srcStr = srcStr.strip().strip(' ,、，,.…~—-;*').lstrip('?？')

    prelude = re.match(re.compile(u'^(甲|乙|黄|汤|A|B|1|2|\[[a-zA-Z])'), srcStr.decode('utf8'))
    if prelude != None:
        return srcStr.lstrip(prelude.group().strip(' 、，,.…~;*').lstrip('?？'))
    return srcStr.strip(' 、，,.…~;*').lstrip('?？')


def FormatSentence(srcData, resultFile):
    resultFp = codecs.open(os.path.join(resultPath, resultFile), 'w', 'utf-8')
    afterRemoveDuplicate = '%s-afterRemoveDuplicate.txt' % str(srcData).split('.')[0]
    RemoveDuplicateLines(srcData, afterRemoveDuplicate)

    srcFp = codecs.open(os.path.join(resultPath, afterRemoveDuplicate), 'r', 'utf-8')
    curLine = srcFp.readline()
    afterStripPrelude = ''
    while curLine:
        afterStripPrelude=StripPrelude(curLine)
        if afterStripPrelude != '':
            afterStripPrelude=StripPrelude(afterStripPrelude)
            resultFp.write(afterStripPrelude.strip() + '\n')
        curLine = srcFp.readline()
    resultFp.close()


if __name__ == '__main__':
    FormatSentence(srcData, resultFile)
