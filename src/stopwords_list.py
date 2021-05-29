import nltk
from nltk.corpus import stopwords
import sys

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")


def printAll() -> None:
    with open("stopwords_list_out.txt", "w") as sys.stdout:
        wordlist = list(stopwords.words('english'))
        count = len(wordlist)
        for i in range(0, count):
            if (i + 1) % 10 == 0 or i == count - 1:
                s = '\n'
            else:
                s = ', '
            print(wordlist[i], end=s)


if __name__ == '__main__':
    printAll()