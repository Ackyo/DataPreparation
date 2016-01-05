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


def FetchUtterance(preNode, curNode, fp):
    question = preNode.text
    # 0到2个汉字+至少0个空格+n个英文问号或感叹号+至少0个空格
    lessThan2WordsPattern = re.compile(u"^ *[\u4e00-\u9fa5]{,2}[\?\!。、，’~]{,5}$")
    lessThan1WordPattern = re.compile(u"^ *[\u4e00-\u9fa5]{,1}[\?\!。、，’]{,5}$")

    # 去除同一个人说的两句话组成的对话、两句相同的话
    if preNode.attrib['speaker'] != curNode.attrib['speaker'] and preNode.text != curNode.text:
        if re.match(lessThan2WordsPattern, str(question).decode('utf8')) == None:
            fp.write(unicode('%s %s\n' % (preNode.attrib['speaker'], preNode.text)))
            fp.write(unicode('%s %s\n' % (curNode.attrib['speaker'], curNode.text)))
            fp.write('\n')
        elif re.match(lessThan1WordPattern, str(question).decode('utf8')) != None:
            print '%s %s\n' % (preNode.attrib['speaker'], preNode.text)
            print '%s %s\n\n' % (curNode.attrib['speaker'], curNode.text)
            oneWordQuestionFp.write(unicode('%s %s\n' % (preNode.attrib['speaker'], preNode.text)))
            oneWordQuestionFp.write(unicode('%s %s\n' % (curNode.attrib['speaker'], curNode.text)))
            oneWordQuestionFp.write('\n')
        elif re.match(re.compile(u"%s{2}" % question[0]),question):
            print '%s %s\n' % (preNode.attrib['speaker'], preNode.text)
            print '%s %s\n\n' % (curNode.attrib['speaker'], curNode.text)
            twoSameWordsQuestionFp.write(unicode('%s %s\n' % (preNode.attrib['speaker'], preNode.text)))
            twoSameWordsQuestionFp.write(unicode('%s %s\n' % (curNode.attrib['speaker'], curNode.text)))
            twoSameWordsQuestionFp.write('\n')
        else:
            print '%s %s\n' % (preNode.attrib['speaker'], preNode.text)
            print '%s %s\n\n' % (curNode.attrib['speaker'], curNode.text)
            twoDiffWordsQuestionFp.write(unicode('%s %s\n' % (preNode.attrib['speaker'], preNode.text)))
            twoDiffWordsQuestionFp.write(unicode('%s %s\n' % (curNode.attrib['speaker'], curNode.text)))
            twoDiffWordsQuestionFp.write('\n')


def FetchAction(preNode, curNode, fp):
    fp.write(unicode('%s\n' % preNode.text))
    fp.write(unicode('%s\n\n' % curNode.text))


data = "D:\PythonProject\剧本数据"
data = unicode(data, "utf-8")

invalidXmlFileFp = codecs.open(u'D:\\PythonProject\\InvalidXmlFile.txt', 'w', 'utf-8')
# noConversation = codecs.open(u'D:\\PythonProject\\noConversation.txt', 'w', 'utf-8')
notHandledFp = codecs.open(u'D:\\PythonProject\\notHandled.txt', 'w', 'utf-8')

oneWordQuestionFp = codecs.open(u'D:\\PythonProject\\oneWordQuestion.txt', 'w', 'utf-8')
twoDiffWordsQuestionFp = codecs.open(u'D:\\PythonProject\\twoDiffWordsQuestion.txt', 'w', 'utf-8')
twoSameWordsQuestionFp = codecs.open(u'D:\\PythonProject\\twoSameWordsQuestion.txt', 'w', 'utf-8')
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
                notHandledFp.write(filePath + '\n')
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

            qaPair = os.path.join(resultPath, '%s-singleQAPair.txt' % str(file).split('.')[0])
            qaPairFp = codecs.open(qaPair, 'w', 'utf-8')

            utteranceCounts = 0
            for curNode in session_node:
                if preNode == 0:
                    preNode = curNode
                    continue
                if curNode.tag == 'utterance':
                    # print curNode.attrib['speaker'], curNode.text
                    FetchUtterance(preNode, curNode, qaPairFp)
                    preNode = curNode
                    utteranceCounts += 1
                    handled = True

            # 处理没有utterance标签，以及仅一个utterance标签和多个action标签的情况
            if handled == False or utteranceCounts == 1:
                if utteranceCounts == 1:
                    session_node = root
                for curNode in session_node:
                    if curNode.tag == 'action':
                        if preNode == 0:
                            preNode = curNode
                            continue
                        # print curNode.text
                        FetchAction(preNode, curNode, qaPairFp)
                        preNode = curNode
                        handled = True
            # 其他特殊情况
            qaPairFp.close()
            if handled == False:
                print '%s not handled' % filePath
                os.remove(qaPair)
                notHandledFp.write(filePath + '\n')

invalidXmlFileFp.close()
notHandledFp.close()
oneWordQuestionFp.close()
twoDiffWordsQuestionFp.close()
twoSameWordsQuestionFp.close()