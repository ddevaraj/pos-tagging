import sys
import time

start_time = time.time()
resultFile = open("hmmmodel.txt","w")
tagWords = []
tagWordsDict = {}
wordDict = {}
tagSeq = {}
emissions = {}
transitions = {}
outTran = {}
tagCount = {}


def main():
    with open(sys.argv[1],encoding="utf-8") as f:
        for line in f:
            wordtags = line.strip().split(" ")
            #print("Length of wordTags", len(wordtags))
            tagWords.append(("<S>","<S>"))
            if "<S>" in tagSeq:
                tagSeq["<S>"].append(wordtags[0][:])
            else:
                tagSeq["<S>"] = [wordtags[0][wordtags[0].rindex("/")+1:]]
            for i,pair in enumerate(wordtags):
                if i!=len(wordtags):
                    slashIndex = pair.rindex("/")
                    word = pair[:slashIndex]
                    tag = pair[slashIndex+1:]
                    if word in wordDict:
                        wordDict[word].add(tag)
                    else:
                        wordDict[word] = set()
                        wordDict[word].add(tag)
                    if tag in tagWordsDict:
                        tagWordsDict[tag].append(word)
                    else:
                        tagWordsDict[tag] = [word]

                    if i+1 < len(wordtags):
                        nextTag = wordtags[i + 1].rindex("/")
                        if tag in tagSeq:
                            tagSeq[tag].append(wordtags[i+1][nextTag+1:])
                        else:
                            tagSeq[tag] = [wordtags[i+1][nextTag+1:]]
                        tagWords.extend([(tag,word)])
                    if i+1 == len(wordtags):
                        tagWords.extend([(tag,word)])
                #print("tagwords",tagWords)
    #print("word",word)
    #print("tag", tag)
    #print("WordDict", wordDict)
    #print("tagWordsDict",tagWordsDict)
    #print("tagWords", tagWords)
    #print("tagSequence", tagSeq)
    zeroTran = {}
    allTags = [tag for (tag,word) in tagWords]
    uniqueTags = set(allTags)
    for tag in uniqueTags:
        zeroTran[tag] = 0
        if tag not in tagSeq:
            tagSeq[tag] = ["<E>"]
    #print("zeroTran", zeroTran)
    words = [word for (tag,word) in tagWords]
    uniqueWords = set(words)

    #print("unique tags", uniqueTags)
    #print("unique words", uniqueWords)

    #Transition numbers
    for tag in tagSeq:
        dict = {}
        myList = tagSeq[tag]
        for givenTag in myList:
            if givenTag in dict:
                dict[givenTag] = dict[givenTag]+ 1
            else:
                dict[givenTag] =1
        transitions[tag] = dict
        outTran[tag] = len(myList)
        #print("transitions", transitions)

    #Emission numbers
    for tag in tagWordsDict:
        myList = tagWordsDict[tag]
        dict = {}
        for word in myList:
            if word in dict:
                dict[word] += 1
            else:
                dict[word] = 1
        emissions[tag] = dict
        tagCount[tag] = len(myList)
        #print("emission", emissions)

    #Smoothing TODO : add smoothing values
    for tag in transitions:
        prob = {}
        prob.update(zeroTran)
        prob.update(transitions[tag])
        transitions[tag] = prob

    try:
        resultFile.write(str(outTran)+"\n")
        resultFile.write(str(tagCount)+"\n")
        resultFile.write(str(emissions) + "\n")
        resultFile.write(str(transitions) + "\n")
        resultFile.write(str(wordDict) + "\n")
        resultFile.write(str(uniqueWords) + "\n")
        resultFile.write(str(uniqueTags) + "\n")
    finally:
        resultFile.close()

if __name__ == "__main__":
    main()
    print("--- %s seconds ---" % (time.time() - start_time))