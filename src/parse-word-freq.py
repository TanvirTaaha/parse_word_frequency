import urllib.request
import urllib.error
import urllib.parse
import nltk
from nltk.corpus import stopwords
import stopwords_list

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

ARTICLE_FILES = {
    "City-Link": [
        "city_link_1.txt",
        "city_link_2.txt"],

    "Pos Lau": ["pos_lau_1.txt",
                "pos_lau_2.txt"],

    "DHL": ["dhl_1.txt"]
}


def wordListToFreqDict(word_list: list) -> dict:
    """
    Counts how many times a word is present in {word_list} for each word in that list
    :param word_list: the list of words to count frequency of
    :return: a dictionary in {'word':'frequency'} format
    :rtype: dict
    """
    word_freq = [word_list.count(p) for p in word_list]
    return dict(list(zip(word_list, word_freq)))


def sortByFreq(freq_dict: dict) -> dict:
    """
    :param: freq_dict: a dictionary of words as keys, and their frequencies as values
    :return: another dictionary which is sorted in descending order of the frequency
    :rtype: dict
    """
    aux = [(freq_dict[key], key) for key in freq_dict]
    aux.sort()
    aux.reverse()
    freq_dict = dict([(y, x) for (x, y) in aux])
    return freq_dict


def stripTags(page_contents: object) -> str:
    """
    :param page_contents: html contents of the page
    :return: a string with all the html tags removed
    :rtype: str
    """
    page_contents = str(page_contents)
    startLoc = page_contents.find("<p>")
    endLoc = page_contents.rfind("<br/>")

    page_contents = page_contents[startLoc:endLoc]

    inside = 0
    _text = ''

    for char in page_contents:
        if char == '<':
            inside = 1
        elif inside == 1 and char == '>':
            inside = 0
        elif inside == 1:
            continue
        else:
            _text += char

    return _text


def stripNonAlphaNum(_text: str) -> list:
    """
    :param _text: a string of multiple sentences, the page-content
    :return: list of all the words inside it
    :rtype: str
    """
    import re
    return re.compile(r'\W+', re.UNICODE).split(_text)


def removeStopWords(wordlist: list, stop_words_list: list) -> list:
    """
    :param wordlist: list of all the words
    :param stop_words_list: list of the stop words that are to be removed
    :return: a list excluding all the stop words
    :rtype: list
    """
    return [w for w in wordlist if w not in stop_words_list]


def sortedDictFromURL(string_url: str) -> dict:
    """
    :param string_url: an url to the webpage
    :return: a dict of words as keys, and their frequencies as values in descending order of frequency
    :rtype: dict
    """
    response = urllib.request.urlopen(string_url)
    html = response.read()
    _text = stripTags(html).lower()
    fullWordList = stripNonAlphaNum(_text)
    wordList = removeStopWords(fullWordList, stopwords.words('english'))
    dictionary = wordListToFreqDict(wordList)
    sortedDict = sortByFreq(dictionary)
    return dict(sortedDict)


def sortedDictFromText(_text: str) -> dict:
    """
    :param _text: a text version of the article
    :return: a dict of words as keys, and their frequencies as values in descending order of frequency
    :rtype: dict
    """
    full_word_list = stripNonAlphaNum(_text)
    word_list = removeStopWords(full_word_list, stopwords.words('english'))
    dictionary = wordListToFreqDict(word_list)
    sorted_dictionary = sortByFreq(dictionary)
    return sorted_dictionary


if __name__ == "__main__":
    for company in ARTICLE_FILES.keys():
        print(company + ": ")
        file_paths = ARTICLE_FILES[company]
        for filepath in file_paths:
            with open(filepath, encoding="utf-8") as file:
                text = file.read()
                print(sortedDictFromText(text))

    stopwords_list.printAll()
