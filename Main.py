import os

from ExtendedFile import ExtendedFile
from Perceptron import Perceptron


def getPerceptrons(languages):
    perceptrons = list()
    for language in languages:
        perceptrons.append(Perceptron(26, 0.2, 1, language, 0.03703703703))

    return perceptrons


def getDictOfFiles(dirPath):
    languages = dict()
    for language in os.listdir(dirPath):
        files = list()
        for file2 in os.listdir(f"{dirPath}/{language}"):
            # tutaj zastanów się nad tym jak chcesz te nazwy przechowywać czy cała ścieżka czy tylko nazwa pliku
            files.append(f"{dirPath}/{language}/{file2}")
        languages[language] = files
    return languages


# gets a vector for a perceptron of a frequency of letters in file
def getVectorDataFromFile(filePath):
    frequencyOfLetters = list()
    for i in range(65, 91):
        tmpLetter, tmpAll = getNumberOfALetterInFile(i, filePath)
        frequencyOfLetters.append(tmpLetter/tmpAll)

    return frequencyOfLetters


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


def getExtendedFiles(languages):
    extendedFiles = list()
    for lang in languages:
        for filePath in languages[lang]:
            extendedFiles.append(ExtendedFile(filePath, lang, getVectorDataFromFile(filePath)))
    return extendedFiles


def initAndReturnGuessCounters(extendedFiles):
    correctGuesses = dict()
    correctGuesses["all"] = 0
    guesses = dict()
    guesses["all"] = 0
    for extendedFile in extendedFiles:
        correctGuesses[extendedFile.language] = 0
        guesses[extendedFile.language] = 0
    return correctGuesses, guesses


def getAccuracyAndTrainPerceptrons(perceptrons, extendedFiles):
    correctGuesses, guesses = initAndReturnGuessCounters(extendedFiles)
    for extendedFile in extendedFiles:
        print(f"\n\n***{extendedFile.filePath}***")
        for perceptron in perceptrons:
            print(f"===============Testing for {perceptron.name} perceptron.===============")
            name = perceptron.name
            answer = perceptron.isActivated(extendedFile.vector)
            correctAnswer = extendedFile.language
            if (not answer and name == correctAnswer) or (answer and name != correctAnswer):
                print("Wrong")
                perceptron.learn(not answer, answer, extendedFile.vector)
            else:
                print("Good")
                correctGuesses["all"] += 1
                correctGuesses[name] += 1
            guesses["all"] += 1
            guesses[name] += 1
    return getAccuracy(correctGuesses, guesses)


def userInputLoop(perceptrons, extendedFiles):
    while True:
        accuracy = getAccuracyAndTrainPerceptrons(perceptrons, extendedFiles)
        printAccuracy(accuracy)

        if input("Continue training? (y/n)") == "n":
            break


def getAccuracy(correctGuesses, guesses):
    accuracy = dict()
    for lang in guesses:
        accuracy[lang] = correctGuesses[lang] / guesses[lang] * 100
    return accuracy


def printAccuracy(accuracy):
    for lang in accuracy:
        print(f"Accuracy for: {lang}:\n{accuracy[lang]}%")


def classificate(answers):
    maxValue = -10
    guess = "I'm not sure."
    for name in answers:
        if answers[name] > maxValue:
            guess = name
            maxValue = answers[name]
    return guess


def main():
    languages = getDictOfFiles("Data/Languages")
    perceptrons = getPerceptrons(languages)
    extendedFiles = getExtendedFiles(languages)

    userInputLoop(perceptrons, extendedFiles)

    # for lang in languages:
    #     for filePath in languages[lang]:
    #         print(filePath)
    #         getFileVectorData(filePath)


# here
main()
