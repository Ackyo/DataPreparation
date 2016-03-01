# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import re
import os
import codecs

def StripPrelude(srcStr):
    try:
        prelude = u'%s' % re.findall(r'^.*?(?= )', srcStr.decode('utf8'))[0].strip()
        return srcStr.decode('utf8').lstrip(prelude).strip()
    except Exception, e:
        print 'Abnormal dialogue:>>>>>>>>>>>%s>>>>>>>>>>>' % srcStr.strip()
    return srcStr.strip()

basePath = os.path.abspath('.')

srcPath = "%s/LabeledData" % basePath
# srcPath = unicode(srcPath, "utf-8")

resultPath = "%s/FinishPreProcess" % basePath
# resultPath = unicode(resultPath, "utf-8")

if os.path.exists(resultPath) == False:
    os.mkdir(resultPath)

if os.path.exists(resultPath) == False:
    os.mkdir(resultPath)

def SplitQAParis2TrainingSet(srcPath, resultPath):
    # 分成两个文件，分别存放合法对话与不合法对话
    validDialogQuestionFileName = 'validDialog-Question.txt'
    validDialogAnswerFileName = 'validDialog-Answer.txt'

    validDialogQuestionPath = os.path.join(resultPath, validDialogQuestionFileName)
    validDialogAnswerPath = os.path.join(resultPath, validDialogAnswerFileName)

    validDialogQuestionFp = codecs.open(validDialogQuestionPath, 'w', 'utf8')
    validDialogAnswerFp = codecs.open(validDialogAnswerPath, 'w', 'utf8')

    validQAPairsFp = codecs.open(os.path.join(resultPath,'validQAParis.txt'),'w','utf8')
    invalidQAPairsFp = codecs.open(os.path.join(resultPath,'invalidQAPairs.txt'),'w','utf8')

    for basePath, dirs, files in os.walk(srcPath):
        singleDialogTotalCount = 0
        singleDialogValidCount = 0
        for file in files:
            filePath = os.path.join(basePath, file)
            # 每次读三行，若前两行都有内容：第三行为1，第三行为0
            print file,':'
            fp = codecs.open(filePath, 'r', 'utf8')
            line1 = fp.readline()
            line2 = fp.readline()
            line3 = fp.readline()

            # print line1,line2,line3

            total=0
            validCount=0

            while line3:
                total += 1
                question = StripPrelude(line1)
                answer = StripPrelude(line2)

                if line3 == '1\n':
                    invalidQAPairsFp.write(question+'\n')
                    invalidQAPairsFp.write(answer+'\n\n')
                else:
                    validCount += 1
                    validDialogQuestionFp.write(question+'\n')
                    validDialogAnswerFp.write(answer+'\n')

                    validQAPairsFp.write(question+'\n')
                    validQAPairsFp.write(answer+'\n\n')

                line1 = fp.readline()
                line2 = fp.readline()
                line3 = fp.readline()
                # print line1,line2,line3
            singleDialogTotalCount += total
            singleDialogValidCount += validCount

            print '<<<<<<< Total:%d  <<<<<< Valid:%d  <<<<<< Invalid: %d <<<<<<' % (total,validCount,total-validCount)
            fp.close()
    print '>>>>>>>>>>>>>>>>>>> Total dialogues: %d >>>>>> Valid: %d >>>>>> Invalid: %d >>>>>>> ValidRate: %.2f%% >>>>>>>>' % (singleDialogTotalCount,singleDialogValidCount,singleDialogTotalCount-singleDialogValidCount,singleDialogValidCount*100.0/singleDialogTotalCount)
    validDialogAnswerFp.close()
    validDialogQuestionFp.close()
    validQAPairsFp.close()
    invalidQAPairsFp.close()


if __name__ == '__main__':
    SplitQAParis2TrainingSet(srcPath, resultPath)
