# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import re
import os
import codecs

basePath = os.path.abspath('.')

srcPath = "%s/QAPairs-BeforeRemoveInvlid" % basePath
# srcPath = unicode(srcPath, "utf-8")

resultPath = "%s/QAPairs-AfterRemoveInvlid" % basePath
# resultPath = unicode(resultPath, "utf-8")

if os.path.exists(resultPath) == False:
    os.mkdir(resultPath)

def StripPrelude(srcStr):
    srcStr=srcStr.strip().strip(' 、，,.…~—-;*').lstrip('?？')
    invalidFormat=False
    try:
        prelude = u'%s' % re.findall(r'^.*?(?= )', srcStr.decode('utf8'))[0].strip()
        return srcStr.decode('utf8').lstrip(prelude).strip(' 、，,.…~;*').lstrip('?？'),invalidFormat
    except Exception, e:
        lackSpace = re.match(re.compile(u'^(甲|乙|黄|汤|A|B|1|2)'),srcStr.decode('utf8'))
        if lackSpace!=None:
            return srcStr.lstrip(lackSpace.group().strip(' 、，,.…~;*').lstrip('?？')),invalidFormat
        else:
            print 'Abnormal dialogue:>>>>>>>>>>>%s>>>>>>>>>>>' % srcStr.strip()
            invalidFormat=True
    return srcStr.strip(' 、，,.…~;*').lstrip('?？'),invalidFormat

def IsInvalidQuestion(question):
# 0到2个汉字+至少0个空格+n个英文问号或感叹号+至少0个空格
    lessThan2WordsPattern = re.compile(u"^ *[\u4e00-\u9fa5]{,2} *[\?\!\，\’\~\-]{,5}(。|、|-|？){,12}$")

    if  re.match(lessThan2WordsPattern, question.decode('utf8')) != None:
        print 'InvalidQuestion: %s\n' % question
        return True
    return False

def IsValidQAPair(question, answer):
    question, invalidQuestionFormat = StripPrelude(question)
    answer, invalidAnswerFormat = StripPrelude(answer)
    if question == None or answer == None or question=='None' or answer=='None':
        return True, question, answer

    if invalidQuestionFormat is True:
        return True, question, answer

    if invalidAnswerFormat is True:
        return True, question, answer

    if IsInvalidQuestion(question):
        return True, question, answer

    return False, question, answer

def RemoveInvalidQAParis(srcPath, resultPath):
    threeWordsPattern = re.compile(u"^ *[\d\u4e00-\u9fa5]{,3}[\?\!。、，’~-—;\'\"“”]{,5}$")
    threeWordsQuestionQAPairs = os.path.join(resultPath,'3WordsQuestionQAPairs.txt')
    threeWordsQuestionFp = codecs.open(threeWordsQuestionQAPairs,'w','utf-8')
    countOf3WordsQuestion = 0
    allDialogues=os.path.join(resultPath,'AllDialogues.txt')
    allFp = codecs.open(allDialogues,'w','utf-8')
    for basePath, dirs, files in os.walk(srcPath):
        singleDialogTotalCount = 0
        singleDialogInvalidCount = 0
        for file in files:
            filePath = os.path.join(basePath, file)
            qaPairAfterRemove = os.path.join(resultPath, '%s.txt' % str(file).split('.')[0])
            qaPairAfterRemoveFp = codecs.open(qaPairAfterRemove, 'w', 'utf-8')
            # 每次读三行，若前两行都有内容：第三行为1，第三行为0
            fp = codecs.open(filePath, 'r', 'utf8')
            line1 = fp.readline()
            line2 = fp.readline()
            line3 = fp.readline()
            print file,':'
            # print line1,line2,line3
            total=0
            invalid = 0
            while line3:
                total += 1
                question = line1
                answer = line2
                isValidQAPair,question,answer=IsValidQAPair(question,answer)
                if isValidQAPair:
                    invalid+=1
                elif re.match(threeWordsPattern, str(question).decode('utf8')) != None:
                    countOf3WordsQuestion+=1
                    threeWordsQuestionFp.write('甲 '+question+'\n')
                    threeWordsQuestionFp.write('乙 '+answer+'\n\n')
                else:
                    qaPairAfterRemoveFp.write('甲 '+question+'\n')
                    qaPairAfterRemoveFp.write('乙 '+answer+'\n\n')
                    allFp.write('甲 '+question+'\n')
                    allFp.write('乙 '+answer+'\n\n')

                line1 = fp.readline()
                line2 = fp.readline()
                line3 = fp.readline()
                # print line1,line2,line3
            singleDialogTotalCount += total
            singleDialogInvalidCount+=invalid
            print '<<<<<<< TotalPairs:%d  <<<<<< Invalid:%d  <<<<<< Valid: %d <<<<<<' % (total,invalid,total-invalid)
            fp.close()
            qaPairAfterRemoveFp.close()
    print '---------------------------------------------------------------\n'
    print 'Count of 3 Words Questions: %d \n'% countOf3WordsQuestion
    print '>>>>>>>>>>>>>>>>>>> Total dialogues: %d >>>>>> Invalid: %d >>>>>> Valid: %d >>>>>>> InvalidRate: %.2f%% >>>>>>>>' % (singleDialogTotalCount,singleDialogInvalidCount,singleDialogTotalCount-singleDialogInvalidCount,singleDialogInvalidCount*100.0/singleDialogTotalCount)
    threeWordsQuestionFp.close()
    allFp.close()


if __name__ == '__main__':
    RemoveInvalidQAParis(srcPath, resultPath)
