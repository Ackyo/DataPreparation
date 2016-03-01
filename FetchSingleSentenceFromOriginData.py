# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import os
import codecs
from xml.etree import ElementTree as ET
import re


def FormatInvalidXmlFile(path, fileName):
    with codecs.open(path, 'r', 'utf-8') as original:
        data0 = original.readline() + original.readline()
        data1 = original.read()

    newFilePath = os.path.join("D:\\PythonProject\\reFormat", 'reformat--%s' % fileName)

    with codecs.open(newFilePath, 'w', 'utf-8') as modified:
        modified.write(data0)
        modified.write('<session>')
        modified.write(data1)
    return newFilePath


def FetchUtterance(curNode, fp):
    fp.write(unicode('%s\n' % curNode.text))
    allSentencesFp.write((unicode('%s\n' % curNode.text)))


def FetchAction(curNode, fp):
    fp.write(unicode('%s\n' % curNode.text))
    allSentencesFp.write((unicode('%s\n' % curNode.text)))


data = "D:\PythonProject\剧本数据"
data = unicode(data, "utf-8")

invalidXmlFileFp = codecs.open(u'D:\\PythonProject\\InvalidXmlFile.txt', 'w', 'utf-8')
# noConversation = codecs.open(u'D:\\PythonProject\\noConversation.txt', 'w', 'utf-8')

resultPath = u'D:\\PythonProject\\AllSentences'

if os.path.exists(resultPath) == False:
    os.mkdir(resultPath)
notHandledFp = codecs.open(os.path.join(resultPath,'notHandledFiles.txt'), 'w', 'utf-8')
GotLessThan10LinesFp = codecs.open(os.path.join(resultPath,'GotLessThan10Lines.txt'), 'w', 'utf-8')

allSentencesFp = codecs.open(os.path.join(resultPath, 'AllSentences.txt'), 'w', 'utf-8')
totalSentences = 0
for basePath, dirs, files in os.walk(data):
    for file in files:
        filePath = os.path.join(basePath, file)

        isValidXmlFile = True
        handled = False
        try:
            tree = ET.parse(filePath)
        except Exception, e:
            # print '>>>>>>>>!!!!!Invalid xml file: (%s)!!!!!!!!<<<<<<<<<' % file
            filePath = FormatInvalidXmlFile(filePath, file)
            try:
                tree = ET.parse(filePath)
            except Exception, e:
                print '%s not handled -- invalid reformat xml file ' % filePath
                notHandledFp.write(filePath + '\n')
                isValidXmlFile == False
                invalidXmlFileFp.write(filePath + '\n')

        if isValidXmlFile == True:
            root = tree.getroot()
            session_node = root.find('session')

            if session_node == None:
                session_node = root[1]

            sentences = os.path.join(resultPath, '%s-Sentences.txt' % str(file).split('.')[0])
            sentencesFp = codecs.open(sentences, 'w', 'utf-8')

            utteranceCounts = 0
            for curNode in session_node:
                if curNode.tag == 'utterance':
                    # print curNode.attrib['speaker'], curNode.text
                    if curNode.text != None:
                        FetchUtterance(curNode, sentencesFp)
                        utteranceCounts += 1
                        handled = True

            # 处理没有utterance标签，以及仅一个utterance标签和多个action标签的情况

            actionCounts = 0
            if handled == False or utteranceCounts <= 3:
                if utteranceCounts == 1:
                    session_node = root
                for curNode in session_node:
                    if curNode.tag == 'action':
                        # print curNode.text
                        if curNode.text != None:
                            FetchAction(curNode, sentencesFp)
                            actionCounts += 1
                            handled = True

            # 其他特殊情况

            fetchedLines = utteranceCounts + actionCounts
            print '%s: %d lines\n' % (file, fetchedLines)
            totalSentences += fetchedLines
            sentencesFp.close()

            if handled == False:
                print '%s not handled' % filePath
                os.remove(sentences)
                notHandledFp.write(filePath + '\n')
            if fetchedLines < 10:
                GotLessThan10LinesFp.write(file + ' %d lines\n' % fetchedLines)

GotLessThan10LinesFp.close()
invalidXmlFileFp.close()
notHandledFp.close()
allSentencesFp.close()
print '------------------------------------\nTotal lines: %d\n' % totalSentences
