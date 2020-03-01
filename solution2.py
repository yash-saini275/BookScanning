class Book(object):
    def __init__(self, id, score):
        self.id = id
        self.score = score
        self.scanned = False

    def getId(self):
        return self.id

    def isScanned(self):
        return self.scanned

    def getScore(self):
        return self.score

    def setScanned(self):
        self.scanned = True

    def __str__(self):
        # output = f'ID: {self.id}, Score: {self.score}\n'
        return str(self.id)

class Library(object):
    def __init__(self, id, timeForSignUp, booksScannedEachDay):
        self.id = id
        self.books = []
        self.timeForSignUp = timeForSignUp
        self.booksScannedEachDay = booksScannedEachDay
        self.signedUp = False
        self.scannedBooks = []
        self.scanIndex = 0

    def getId(self):
        return self.id

    def getBooks(self):
        return self.books

    def getTimeForSignUp(self):
        return self.timeForSignUp

    def getBooksScannedEachDay(self):
        return self.booksScannedEachDay

    def getScannedBooks(self):
        return self.scannedBooks

    def setSignedUp(self):
        self.signedUp = True

    def sortBooks(self):
        self.books.sort(key=lambda book: book.getScore(), reverse=True)

    def sendBooks(self):
        if self.signedUp:
            choosenBooks = []
            while (len(choosenBooks) < self.booksScannedEachDay):
                try:
                    if not(self.books[self.scanIndex].isScanned()):
                        choosenBooks.append(self.books[self.scanIndex])
                        self.books[self.scanIndex].setScanned()
                    self.scanIndex += 1
                except IndexError:
                    break
            # for book in self.books:
            #     if (not(book.isScanned) and (len(choosenBooks) <= self.booksScannedEachDay)):
            #         choosenBooks.append(book)
            #     if len(choosenBooks) == self.booksScannedEachDay:
            #         break
            self.scannedBooks += choosenBooks

    def __str__(self):
        output = f'ID: {self.id}\nBooks: {self.books}\nTime for SignUp: {self.timeForSignUp}\n'
        return output

class SignUp(object):
    def __init__(self):
        self.signingUp = False
        self.library = None
        self.numberOfDaysRemaining = None

    def signUpLibrary(self):
        self.signingUp = False
        library = self.library
        self.library = None
        return library

    def isSigningUp(self):
        return self.signingUp

    def getNumberOfDaysRemaining(self):
        return self.numberOfDaysRemaining

    def setLibraryAndNumberOfDays(self, library):
        for book in library.getBooks():
            if not(book.isScanned()):
                flag = True
        if flag:
            self.signingUp = True
            self.library = library
            self.numberOfDaysRemaining = library.getTimeForSignUp()

    def decNumberOfDaysRemaining(self):
        self.numberOfDaysRemaining -= 1
        if self.numberOfDaysRemaining == 0:
            return self.signUpLibrary()
        return None

    def __str__(self):
        output = f'Library: {self.library}\nNumber of Days Remaining to Sign Up: {self.numberOfDaysRemaining}'
        return output

class SignedUpLibraries(object):
    def __init__(self):
        self.signedUpLibraries = []

    def addLibrary(self, library):
        library.setSignedUp()
        self.signedUpLibraries.append(library)

    def getLibraries(self):
        return self.signedUpLibraries

    def removeLibraries(self):
        for library in self.signedUpLibraries:
            if len(library.getScannedBooks()) == 0:
                self.signedUpLibraries.remove(library)

def createBooks(bookScores):
    books = []
    Id = 0
    for score in bookScores:
        books.append(Book(Id, score))
        Id += 1
    return books

def addBooksToLibrary(books, bookIds):
    booksToAdd = []
    for bookId in bookIds:
        booksToAdd.append(books[bookId])
    return booksToAdd

def createBooksAndLibraries(fileName):
    f = open(fileName, 'r')
    B, L, D = map(int, f.readline().split(' '))
    bookScores = map(int, f.readline().split(' '))
    books = createBooks(bookScores)
    libraries = []
    for Id in range(L):
        N, T, M = map(int, f.readline().split(' '))
        booksInLibrary = map(int, f.readline().split(' '))
        library = Library(Id, T, M)
        library.books = addBooksToLibrary(books, booksInLibrary)
        library.sortBooks()
        libraries.append(library)
    f.close()
    return (books, libraries, D)

def signUpAndScanBooks(libraries, numberOfDays):
    signUp = SignUp()
    signedUpLibraries = SignedUpLibraries()
    libraryIndex = 0
    for day in range(numberOfDays):
        try:
            while not(signUp.isSigningUp()):
                signUp.setLibraryAndNumberOfDays(libraries[libraryIndex])
                libraryIndex += 1
        except IndexError:
            pass

        for signedUpLibrary in signedUpLibraries.getLibraries():
            signedUpLibrary.sendBooks()

        signUpLibrary = signUp.decNumberOfDaysRemaining()

        if signUpLibrary != None:
            signedUpLibraries.addLibrary(signUpLibrary)
    return signedUpLibraries


def makeOutput(fileName, signedUpLibraries):
    outputFileName = fileName[:-4] + '_output.txt'
    print(outputFileName)
    f = open(outputFileName, 'w')
    signedUpLibraries.removeLibraries()
    f.write(str(len(signedUpLibraries.getLibraries())) + '\n')
    for library in signedUpLibraries.getLibraries():
        f.write(str(library.getId()) + ' ' + str(len(library.getScannedBooks())) + '\n')
        bookIds = [str(bookId) for bookId in library.getScannedBooks()]
        f.write(' '.join(bookIds) + '\n')
    f.close()
    print("Created File: ", outputFileName)


def main():
    fileNames = ['a_example.txt','b_read_on.txt','c_incunabula.txt','d_tough_choices.txt', 'e_so_many_books.txt','f_libraries_of_the_world.txt']
    fileNames = ['d_tough_choices.txt']
    for fileName in fileNames:
        books, libraries, numberOfDays = createBooksAndLibraries(fileName)
        libraries = sorted(libraries, key=lambda library:library.getTimeForSignUp())
        signedUpLibraries = signUpAndScanBooks(libraries, numberOfDays)
        makeOutput(fileName, signedUpLibraries)

if __name__=='__main__':
    main()