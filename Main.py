import os
import random

from ExtendedFile import ExtendedFile
from Perceptron import Perceptron


def getPerceptrons(languages):
    perceptrons = list()
    for language in languages:
        perceptrons.append(Perceptron(26, 0.15, 0.2, language, 0.03703703703))

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
def getVectorDataFromFileOrString(filePathOrString, fileOrString):
    frequencyOfLetters = list()
    for i in range(65, 91):
        if fileOrString:
            tmpLetter, tmpAll = getNumberOfALetterInFile(i, filePathOrString)
        else:
            tmpLetter, tmpAll = getNumberOfALetterInLine(i, filePathOrString)
        frequencyOfLetters.append(tmpLetter/tmpAll)
    return frequencyOfLetters


def getNumberOfALetterInLine(letterInAscii, line):
    countOfLetter = 0
    countOfAll = 0
    line = line.upper()
    for c in line:
        if c == chr(letterInAscii):
            countOfLetter += 1
        countOfAll += 1
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
    blockLength = 10000000
    for lang in languages:
        if len(languages[lang]) < blockLength:
            blockLength = len(languages[lang])
        for filePath in languages[lang]:
            extendedFiles.append(ExtendedFile(filePath, lang, getVectorDataFromFileOrString(filePath, True)))

    reshuffledExtendedFiles = list()
    for i in range(blockLength):
        for j in range(0, len(extendedFiles), blockLength):
            reshuffledExtendedFiles.append(extendedFiles[i+j])

    return reshuffledExtendedFiles


def initAndReturnGuessCounters(extendedFiles):
    correctGuesses = dict()
    correctGuesses["All"] = 0
    guesses = dict()
    guesses["All"] = 0
    for extendedFile in extendedFiles:
        correctGuesses[extendedFile.language] = 0
        guesses[extendedFile.language] = 0
    return correctGuesses, guesses


def getAccuracyAndTrainPerceptrons(perceptrons, extendedFiles):
    correctGuesses, guesses = initAndReturnGuessCounters(extendedFiles)
    # random.shuffle(extendedFiles)

    for extendedFile in extendedFiles:
        # print()
        for perceptron in perceptrons:
            name = perceptron.name
            answer = perceptron.isActivated(extendedFile.vector)
            correctAnswer = extendedFile.language
            if (not answer and name == correctAnswer) or (answer and name != correctAnswer):
                perceptron.learn(not answer, answer, extendedFile.vector)
            else:
                correctGuesses["All"] += 1
                if answer:
                    correctGuesses[name] += 1
            guesses["All"] += 1
            if name == correctAnswer:
                guesses[name] += 1
    return getAccuracy(correctGuesses, guesses)


def trainNTimes(perceptrons, extendedFiles, n):
    accuracy = dict()
    for i in range(n):
        accuracy = getAccuracyAndTrainPerceptrons(perceptrons, extendedFiles)

    printAccuracy(accuracy)


def userInputLoop(perceptrons, extendedFiles):
    n = 1
    while True:
        for i in range(10):
            print(f"\nAge number: {n}.")
            n += 1
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
        print(f"Accuracy for {lang}:\n{accuracy[lang]}%")


def classificate(answers):
    maxValue = -1000000
    guess = "I'm not sure."
    for name in answers:
        print(f"{name}:{answers[name]}")
        if answers[name] > maxValue:
            guess = name
            maxValue = answers[name]
    return guess


def checkUserInput(perceptrons):
    while True:
        print("Please give me your text to check:")
        inputToCheck = getMultilineInput()
        vector = getVectorDataFromFileOrString(inputToCheck, False)
        print()
        print()

        answers = dict()
        for perceptron in perceptrons:
            answers[perceptron.name] = perceptron.getActivationValue(vector)

        myGuess = classificate(answers)

        print(f"I think this text is written in: {myGuess}")

        if input("Do you want to check another text? (y/n)") == "n":
            break


def printPerceptronValues(perceptrons):
    for perceptron in perceptrons:
        perceptron.printInfo()


def getMultilineInput():
    lines = []
    go = False
    while True:
        line = input()
        if line:
            go = False
            lines.append(line)
        else:
            if go:
                break
            go = True
    return "\n".join(lines)


def main():
    languages = getDictOfFiles("Data/Languages")
    perceptrons = getPerceptrons(languages)
    extendedFiles = getExtendedFiles(languages)

    userInputLoop(perceptrons, extendedFiles)
    # trainNTimes(perceptrons, extendedFiles, 20)

    printPerceptronValues(perceptrons)

    checkUserInput(perceptrons)


# here
main()
