# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# This demo can extract the TF-IDF features of each big class data.
# We further use k words  corresponding to the k bigges weights as the features set for each big class.

import IndexOfClass  # import the IndexOfClass.py, to obtain the row index of each big class in the original Rujia data
import math  # the math.log10 is in this module

fileTF = open('TF features.txt', 'w')

numBigClass = len(IndexOfClass.dictClassR_C) - 1

for index in range(1, numBigClass + 1):  # 1, numBigClass+1
    print 'the ' + str(index) + ' class is processing...'
    fileRujia = open('Data_After_Split.txt', 'r')  # open the original Rujia data file
    dictTF_IDF = {}
    wordSum = 0  # mark the sum of frequency of words, i.e. the denumerator of TF

    rowHead = IndexOfClass.dictClassR_C[index]  # head row of the index class
    rowTail = IndexOfClass.dictClassR_C[index + 1]  # tail row
    for line in fileRujia.readlines()[rowHead - 1:rowTail - 1]:  # within the index class
        # print rowHead, rowTail
        # print line
        for word in line.split():  # this FOR loop counts the term times
            wordSum += 1
            if dictTF_IDF.has_key(word):
                dictTF_IDF[word] += 1
            else:
                dictTF_IDF[word] = 1

    for word in dictTF_IDF:
        dictTF_IDF[word] = 1.0 * dictTF_IDF[word] / wordSum  # to obtain the TF

        numDocument = 1
        for k in range(1, numBigClass + 1):  # search for the number of big class containing the current word
            r1 = IndexOfClass.dictClassR_C[k]
            r2 = IndexOfClass.dictClassR_C[k + 1]
            # print r1, r2
            fileRujia = open('Data_After_Split.txt', 'r')
            for line in fileRujia.readlines()[r1 - 1:r2 - 1]:
                # print line
                if word in line.split():
                    numDocument += 1
                    # print 'abc'
                    break
                    # print numDocument
        dictTF_IDF[word] *= math.log10(1.0 * numBigClass / numDocument)  # IDF

    L = sorted(dictTF_IDF.iteritems(), key=lambda asd: asd[1], reverse=True)
    for k in L[0:5]:
        fileTF.write(k[0] + ' ' + str(k[1]) + ' ')
    fileTF.write('\n')
