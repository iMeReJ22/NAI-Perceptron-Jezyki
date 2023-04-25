class ExtendedFile:
    def __init__(self, filePath, language, vector):
        self.filePath = filePath
        self.language = language
        self.vector = vector

    def __str__(self):
        return self.filePath
