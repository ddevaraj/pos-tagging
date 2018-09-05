import time
import sys
start_time = time.time()
file = open("hmmmodel.txt").read()
data = file.split("\n")
transitionLen = eval(data[0])
emissionLen = eval(data[1])
tagWordsDict = eval(data[2])
tagDict = eval(data[3])
wordDict = eval(data[4])
uniqueWords = eval(data[5])
uniqueTags = eval(data[6])
outputFile = open("hmmoutput.txt","w")
def main():
    with open(sys.argv[1]) as f:
        for line in f:
            wordToBeTagged = line.split()
            #sentLen = len(wordToBeTagged)
            firstTransition = {}
            firstBackpointer = {}
            viterbi = []
            backPointers = []
            if wordToBeTagged[0] in uniqueWords:
                tagList = wordDict[wordToBeTagged[0]]
            else:
                tagList = uniqueTags

            for tag in tagList:
                if tag == "<S>":
                    continue
                transitionProb = float(tagDict['<S>'][tag] + 1)/float(len(tagDict['<S>']) + transitionLen['<S>'])
                if wordToBeTagged[0] in uniqueWords:
                    emissionProb = float(tagWordsDict[tag][wordToBeTagged[0]])/emissionLen[tag]
                    firstTransition[tag] = transitionProb*emissionProb
                else:
                    firstTransition[tag] = transitionProb
                firstBackpointer[tag] = "<S>"

            viterbi.append(firstTransition)
            backPointers.append(firstBackpointer)

            ''''#result = findBestVal(firstTransition)
            max = 0.0
            currbest = list(firstTransition.keys())[0]
            for tag in firstTransition.keys():
                if firstTransition[tag] >= max:
                    max = firstTransition[tag]
                    currbest = tag'''

            for index in range(1,len(wordToBeTagged)):
                presentTransition = {}
                presentBP = {}
                previousBP = viterbi[-1]
                if wordToBeTagged[index] in uniqueWords:
                    tagList = wordDict[wordToBeTagged[index]]
                else:
                    tagList = uniqueTags
                for tag in tagList:
                    if tag == "<S>":
                        continue
                    if wordToBeTagged[index] in uniqueWords:
                        word = wordToBeTagged[index]
                        prevBestTag = list(previousBP.keys())[0]
                        maxVal = 0.0
                        emProb = 0.0
                        for prevTag in previousBP.keys():
                            #print("HLEP", tagWordsDict)
                            #print("emisison", emissionLen)
                            #print("emission tag", emissionLen[tag])
                            #print("tag -- ", tag)
                            #print("word",wordToBeTagged[index])
                            #print("word to be tagged",tagWordsDict[tag][wordToBeTagged[index]])
                            prob = calcViterbi(previousBP,prevTag,tag, wordToBeTagged,index)
                            emProb = float(tagWordsDict[tag][wordToBeTagged[index]])/float(emissionLen[tag])
                            val = prob * emProb
                            #val = previousBP[prevTag] * float(tagDict[prevTag][tag] + 1) / float(len(tagDict[prevTag]) + transitionLen[prevTag])*float(tagWordsDict[tag][wordToBeTagged[index]])/float(emissionLen[tag])
                            if val >= maxVal:
                                maxVal=val
                                prevBestTag = prevTag
                        val1 = calcViterbi(previousBP,prevBestTag,tag, wordToBeTagged,index)
                        #val1 = previousBP[prevTag] * float(tagDict[prevTag][tag] + 1) / float(len(tagDict[prevTag]) + transitionLen[prevTag])*float(tagWordsDict[tag][wordToBeTagged[index]])/float(emissionLen[tag])
                        presentTransition[tag] = val1*emProb
                    else:
                        word = wordToBeTagged[index]
                        prevBestTag = list(previousBP.keys())[0]
                        maxVal = 0.0
                        for prevTag in previousBP.keys():
                            val = calcViterbi(previousBP, prevTag, tag, wordToBeTagged,index)
                            if val >= maxVal:
                                maxVal = val
                                prevBestTag = prevTag
                        presentTransition[tag] = calcViterbi(previousBP,prevBestTag,tag, wordToBeTagged,index)
                    presentBP[tag]=prevBestTag

                result = findBestVal(presentTransition)
                max = result[0]
                currbest = result[1]
                viterbi.append(presentTransition)
                backPointers.append(presentBP)
            previousBP = viterbi[-1]
            prevBestTag = list(previousBP.keys())[0]
            max = 0.0
            for prevTag in previousBP.keys():
                val = previousBP[prevTag] * float(tagDict[prevTag][currbest] + 1)/float(len(tagDict[prevTag]) + transitionLen[prevTag])
                if val>=max:
                    max = val
                    prevBestTag = prevTag

            prob_tagsequence = previousBP[prevBestTag] * float(tagDict[prevBestTag][currbest] + 1) / float(len(tagDict[prevBestTag]) + transitionLen[prevBestTag])
            best_tagsequence = [prevBestTag]
            backPointers.reverse()
            currBestTag = prevBestTag
            for bp in backPointers:
                best_tagsequence.append(bp[currBestTag])
                currBestTag = bp[currBestTag]

            best_tagsequence.reverse()
            best_tagsequence.pop(0)
            count = 1
            for w, t in zip(wordToBeTagged, best_tagsequence):
                if count < len(wordToBeTagged):
                    outputFile.write(w + "/" + t + " ")
                    count += 1
                else:
                    outputFile.write(w + "/" + t)
            outputFile.write("\n")


    #print("Viterbi", viterbi)
    #print("Backpointer", backPointers)

def calcViterbi(previousBP,prevTag,tag, wordToBeTagged,index):
    val = previousBP[prevTag] * float(tagDict[prevTag][tag] + 1) / float(len(tagDict[prevTag]) + transitionLen[prevTag])
    return val

def findBestVal(viterbiKey):
    maxVal = 0.0
    bestTag = list(viterbiKey.keys())[0]
    for tag in viterbiKey.keys():
        if viterbiKey[tag]>= maxVal:
            maxVal=viterbiKey[tag]
            bestTag = tag
    return maxVal,bestTag



if __name__ == "__main__":
    main()
    print("--- %s seconds ---" % (time.time() - start_time))