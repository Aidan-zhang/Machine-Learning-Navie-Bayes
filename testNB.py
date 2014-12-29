'''Created on April12, 2014
Navie Bayes classify algorithm, multinomial model and bernoulli model test
@author: Aidan
'''
from numpy import *
from object_json import *
from naviebayes import *
import pdb

def textParse(bigString):    #input is big string, #output is word list
    import re
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def loadDataSet():      #general function to parse tab -delimited floats
     docList = [];classList = [];fullText = []
     for i in range(1,26):# create train Doc list
        with open('email/spam/%d.txt'%i, 'r') as fr:
            wordlist = textParse(fr.read())
        docList.append(wordlist)
        fullText.extend(wordlist)
        classList.append('spam')

        with open('email/ham/%d.txt'%i, 'r') as fr:
            wordlist = textParse(fr.read())
        docList.append(wordlist)
        fullText.extend(wordlist)
        classList.append('ham')
     return docList, classList, fullText

def crossValidateIndexGet(samplecount, testcount):
     '''randomly pick testcount index as test data index'''
     trainSet =range(samplecount);testSet = []
     for i in range(testcount):
         randIndex = int(random.uniform(0,len(trainSet)))
         testSet.append(trainSet[randIndex])
         del(trainSet[randIndex])
     return trainSet, testSet

def crossValidateDataSplit(docList, classList, testcount = 10):
    samplecount = len(docList)
    trainIndex, testIndex = crossValidateIndexGet(samplecount, testcount)
    ''' create train sequence'''
    trainDocsList = [ docList[docIndex] for docIndex in trainIndex]
    trainClassesList = [classList[docIndex] for docIndex in trainIndex]

    '''test the train sequence with testSet'''
    testDocsList = [docList[i] for i in testIndex]
    testclassesList = [classList[i] for i in testIndex]

    return trainDocsList, trainClassesList, testDocsList, testclassesList

def NBTest():
    docList, classList,fullTextList = loadDataSet()
    #laplaceFactor = [1, 0.5, 0.1, 0.01, 0.001, 0.00001]
    laplaceFactor = [1]
    testcount = 10
    NBclassifier = navieBayes()

    trainDocsList, trainClassesList, testDocsList, testclassesList = \
                   crossValidateDataSplit(docList, classList, testcount)
    for lf in laplaceFactor:
        NBclassifier.trainNB(docList, classList,lapFactor = lf)
        NBclassifier.trainNB(docList, classList, modelType = 'bernoulli', lapFactor = lf)
        predictClass_mul = []
        errorCount = 0.0
        for i in range(testcount):
            #predictClass = NBclassifier.classifyNB(testDocsList[i], modelType = 'multinomial')
            predictClass = NBclassifier.classifyNB(testDocsList[i], modelType = 'bernoulli')
            predictClass_mul.append(predictClass)
            if predictClass != testclassesList[i]:
                errorCount+=1
                print 'the real class is %s, the predict class is %s'%(testclassesList[i], predictClass)
        print 'the error count with laplaceFactor %s is %s'%(lf, errorCount)
        #pdb.set_trace()

if __name__ == '__main__':
    
    NBTest()
