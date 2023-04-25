import os

from Perceptron import Perceptron


def getPerceptrons(languages2):
    perceptrons2 = list()
    for language in languages2:
        perceptrons2.append(Perceptron(27, 0.2, 1, language, 0.03703703703))

    return perceptrons2


def getDictionaryOfFiles(dirPath):
    languages2 = dict()
    for language in os.listdir(dirPath):
        files = list()
        for file2 in os.listdir(f"{dirPath}/{language}"):
            # tutaj zastanów się nad tym jak chcesz te nazwy przechowywać czy cała ścieżka czy tylko nazwa pliku
            files.append(f"{dirPath}/{language}/{file2}")
        languages2[language] = files
    return languages2


# gets a vector for a perceptron of a frequency of letters in file
def getFileVectorData(filePath):
    nOfLetters = dict()
    for i in range(65, 91):
        tmpLetter, tmpAll = getNumberOfALetterInFile(i, filePath)
        nOfLetters[chr(i)] = tmpLetter/tmpAll

    print(nOfLetters)


def getNumberOfALetterInLine(letterInAscii, line):
    countOfLetter = 0
    countOfAll = 0
    line = line.upper()
    for c in line:
        if c == chr(letterInAscii):
            countOfLetter += 1
        countOfAll +=1
    return countOfLetter, countOfAll


def getNumberOfALetterInFile(letterInAscii, filePath):
    file = open(filePath, "r", encoding="utf8")
    countOfLetter = 0
    countOfAll = 0

    for line in file:
        tmpLetter, tmpAll = getNumberOfALetterInLine(letterInAscii, line)
        countOfLetter += tmpLetter
        countOfAll += tmpAll
    file.close()
    return countOfLetter, countOfAll


# main code
languages = getDictionaryOfFiles("Data/Languages")
perceptrons = getPerceptrons(languages)

getFileVectorData("Data/Languages/English/1.txt")
