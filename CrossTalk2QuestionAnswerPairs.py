# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import os
import codecs
from xml.etree import ElementTree as ET

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


def FetchUtterance(preNode, curNode, fp):
    if preNode.attrib['speaker'] != curNode.attrib['speaker']:
        fp.write(unicode('%s %s\n' % (preNode.attrib['speaker'], preNode.text)))
        fp.write(unicode('%s %s\n' % (curNode.attrib['speaker'], curNode.text)))
        fp.write('\n')

def FetchAction(preNode, curNode, fp):
    fp.write(unicode('%s\n' % preNode.text))
    fp.write(unicode('%s\n' % curNode.text))

data = "D:\PythonProject\剧本数据"
data = unicode(data, "utf-8")

invalidXmlFileFp = codecs.open(u'D:\PythonProject\InvalidXmlFile.txt', 'w', 'utf-8')
# noConversation = codecs.open(u'D:\\PythonProject\\noConversation.txt', 'w', 'utf-8')
notHandledFp = codecs.open(u'D:\\PythonProject\\notHandled.txt', 'w', 'utf-8')

resultPath = u'D:\\PythonProject\\QAPairs'

if os.path.exists(resultPath) == False:
    os.mkdir(resultPath)


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
                notHandledFp.write(filePath+'\n')
                isValidXmlFile == False
                invalidXmlFileFp.write(filePath + '\n')

        if isValidXmlFile == True:
            root = tree.getroot()
            session_node = root.find('session')

            if session_node == None:
                session_node = root[1]

            # if session_node == None:
            #     print '>>>>>>>>!!!!!no conversation?: (%s)!!!!!!!!<<<<<<<<<<<<<<<<' % file
            #     noConversation.write(filePath + '\n')
            # else:

            preNode = 0

            qaPair=os.path.join(resultPath, '%s-singleQAPair.txt' % str(file).split('.')[0])
            qaPairFp = codecs.open(qaPair, 'w', 'utf-8')

            utteranceCounts = 0
            for curNode in session_node:
                if preNode == 0:
                    preNode = curNode
                    continue
                if curNode.tag == 'utterance':
                    # print curNode.attrib['speaker'], curNode.text
                    FetchUtterance(preNode, curNode, qaPairFp)
                    preNode=curNode
                    utteranceCounts += 1
                    handled=True
                    # elif curNode.tag == 'action':
                    #     print curNode.text
                    #     FetchAction(preNode, curNode, queryAnswerPairs)
                    # else:
                        # print '******************************** not Find: (%s) **************************************' % filePath
            #处理没有utterance标签，以及仅一个utterance标签和多个action标签的情况
            if handled == False or utteranceCounts==1:
                if utteranceCounts==1:
                    session_node=root
                for curNode in session_node:
                    if curNode.tag == 'action':
                        if preNode == 0:
                            preNode = curNode
                            continue
                        # print curNode.text
                        FetchAction(preNode, curNode, qaPairFp)
                        preNode=curNode
                        handled = True
            #其他特殊情况
            qaPairFp.close()
            if handled == False:
                print '%s not handled' % filePath
                os.remove(qaPair)
                notHandledFp.write(filePath+'\n')

invalidXmlFileFp.close()
notHandledFp.close()
