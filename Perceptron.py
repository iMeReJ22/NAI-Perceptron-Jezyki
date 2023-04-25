class Perceptron:
    def __init__(self, weightVectorLength, a, threshold, name, startValuesOfWeights):
        self.weights = list()
        self.__initWeightsList(weightVectorLength, startValuesOfWeights)
        self.a = a
        self.threshold = threshold
        self.name = name
        # self.printInfo()

    def isActivated(self, vector):
        if len(vector) != len(self.weights):
            exit("Wrong vector length.")
        return self.__getSum(vector) >= self.threshold

    def getActivationValue(self, vector):
        if len(vector) != len(self.weights):
            exit("Wrong vector length.")
        return self.__getSum(vector) - self.threshold

    def learn(self, expected, recived, vector):
        # (expected - recived) * alfa = X
        # weights[prog] + (expected - recived) * alfa * vector[-1(y)]
        X = (expected - recived) * self.a
        vector = list(map(lambda x: x * X, vector))

        for i in range(len(vector)):
            self.weights[i] += vector[i]

        self.threshold += X * -1

    def __initWeightsList(self, n, start):
        for i in range(n):
            self.weights.append(start)

    def __getSum(self, vector):
        sum = 0
        for i in range(len(vector)):
            sum += vector[i] * self.weights[i]
        return sum

    def printInfo(self):
        print(f"\nCurrent values for {self.name}")
        print("Weights:\n" + self.weights.__str__())
        print(f"Threshold:\t{self.threshold}")
