# import sec downloader
from sec_edgar_downloader import Downloader
# import os module to clear screen
import os
# import shutil to move files
import shutil
# import beautiful soup to parse html
from bs4 import BeautifulSoup
# import string module to retrieve digits
import string
# import most common words
from nltk.corpus import stopwords
# import urllib to open links
from urllib.request import urlopen
# import math for square root and log
import math

# create downloader object
download = Downloader()

# define companies to download
companies = ["AAPL", "MSFT", "TWTR"]

# define list of text to parse
parse_text = []

# define list to store word counts
count_lst = []

# define glossary
glossary = []

# create dictionary for frequencies of words
freqs = {}

# clear screen
def clear_screen():
    # repeat 4 times
    for i in range(4):
        # clear screen
        os.system("clear")

# remove substrings from text
def remove_substrings(text, substrings):

    # add punctuation to substrings
    substrings += string.punctuation

    # loop through substrings
    for s in substrings:
        # remove substring
        text = "".join(text.split(s))

    # return text
    return text

# remove whitespace from text
def remove_whitespace(text):

    # define whitespaces
    whitespaces = string.whitespace

    # remove whitespace
    text = text.strip()

    # loop through whitespaces
    for w in whitespaces:
        # remove whitespace
        text = " ".join(text.split(w))

    # return text
    return text

# check if word includes digit
def includes_digit(word, digits):
    # loop through characters
    for c in word:
        # if character is digit
        if c in digits:
            # return true
            return True

    # if there are no digits in word, return false
    return False

# remove numbers from text
def remove_num(text):

    # define digits
    digits = list(string.digits)

    # define new text
    new_text = []

    # loop through words
    for w in text.split():
        # if word does not include a digit
        if not includes_digit(w, digits):
            # add word
            new_text.append(w)

    # return new text
    return " ".join(new_text)

# remove most common words
def remove_stop_words(text):

    # define new text
    new_text = []

    # loop through words
    for w in text.split():
        # if word is not common
        if w not in stopwords.words("english"):
            # add word
            new_text.append(w)

    # return new text
    return " ".join(new_text)

# parse files
def parse_files():
    # for filename in directory
    for fname in os.listdir("Files"):

        # if filename starts with "."
        if fname.startswith("."):
            # invalid, go to next file
            continue

        # define path
        path = os.path.join("Files", fname)

        # open file to read
        with open(path, "r") as file:
            # read file
            text = file.read()
            # make lowercase
            lower = text.lower()

            # split text by slicing after item 1a
            bottom = lower.split("item 1a. ")[1]
            # split text by slicing before item 1b
            final = bottom.split("item 1b. ")[0]

            # use beautiful soup
            soup = BeautifulSoup(final, "html.parser")

            # remove symbols from text
            formatted = remove_substrings(soup.text, ["\n", " | 2021 form 10-k | ", "•", "’", "”", "“", ";"])

            # remove whitespace
            formatted = remove_whitespace(formatted)

            # remove numbers
            formatted = remove_num(formatted)

            # remove most common words
            formatted = remove_stop_words(formatted)

            # add text to list
            parse_text.append(formatted)

# format glossary word
def format_glossary(text):

    # make text lwoercase
    text = text.lower()

    # define characters to remove
    lst = ["                         ", "                          ", "\n"]

    # loop through characters
    for c in lst:
        # remove character
        text = "".join(text.split(c))
        # remove whitespace
        text = text.strip()

    return text

# retrieve possible words from word with parentheses
def return_possible_words(word):
    # define dictionary of characters and what to replace with
    chars = {"( r)": "r", "(s)": "s"}

    # define list of words to return
    return_lst = []

    # loop through characters
    for orig, new in chars.items():

        # if word contains character
        if orig in word:
            # retrieve first word
            first = "".join(word.split(orig))
            # retrieve second word
            second = new.join(word.split(orig))
            # add first word to lst
            return_lst.append(first)
            # add second word to lst
            return_lst.append(second)

    # return lst
    return return_lst

# retrieve cybersecurity glossary
def get_cyber_words():
    # define variable to store data
    data = ""
    # open glossary to read
    with open("glossary.html", "r") as file:
        # retrieve data
        data = file.read()

        # use BeautifulSoup
    soup = BeautifulSoup(data, "html.parser")

    # retrieve words
    tags = soup.find_all("dt")

    # loop through tags
    for tag in tags:

        # format glossary word
        formatted = format_glossary(tag.text)

        # if word isn't already there
        if formatted not in glossary:

            # if there is a slash
            if " / " in formatted:
                # loop through each word
                for w in formatted.split(" / "):
                    # add word to glossary
                    glossary.append(w)
            # if there is (r) or (s)
            elif "( r)" in formatted or "(s)" in formatted:
                # retrieve first possible word
                first = return_possible_words(formatted)[0]
                # retrieve second possible word
                second = return_possible_words(formatted)[1]
                # add first word to glossary
                glossary.append(first)
                # add second word to glossary
                glossary.append(second)
            # if there is an acronym
            elif " (" in formatted:
                # retrieve first word
                first = formatted.split(" (")[0]
                # retrieve second word
                second = formatted.split(" (")[1]
                # remove parentheses
                second = second.split(")")[0]
                # add first word to glossary
                glossary.append(first)
                # add second word to glossary
                glossary.append(second)
            # otherwise
            else:
                # add formatted word to glossary
                glossary.append(formatted)

    # sort glossary
    glossary.sort()

# weight rare words heavier than common words
def weight(freq):
    # increase weight for rare words
    return math.sqrt(1/freq)

# calculate word frequencies
def word_freq():
    # set total number of words to 1 trillion
    total_num = 10 ** 12
    # open words file
    with open("all_words.csv", "r") as file:

        # loop through lines
        for l in file:

            # retrieve word
            word = l.split(",")[0]

            # if word is not cyber-related
            if word not in glossary:
                # skip it
                continue

            # retrieve frequency
            freq = l.split(",")[1]
            # convert frequency to integer
            freq = int(freq)
            # calculate percent frequency
            pct_freq = freq/total_num * 100
            # weight frequency
            freq = weight(pct_freq)
            # add word & frequency to dictionary
            freqs[word] = freq

# retrieve highest weighted frequency
def max_freq():

    # define max frequency
    max = -1

    # loop through dictionary
    for w, f in freqs.items():
        # if current frequency is greater
        if f > max:
            # update max
            max = f

    # return max
    return max

# calculate score
def calc_score(term):

    # if term is common
    if term in freqs.keys():
        # return weighted frequency
        return freqs[term]

    # split by words
    lst = term.split()

    # if term is 1 word and rare
    if len(lst) < 2:
        # return max frequency
        return max_freq()

    # set score to 0
    score = 0

    # loop through words
    for w in lst:
        # if word is common
        if w in freqs.keys():
            # increment by weighted frequency
            score += freqs[w]
        # if word is rare
        else:
            # increment by max frequency
            score += max_freq()

    # return score
    return score

# adjust score depending on text length
def adjust_score(score, text):
    # retrieve number of words
    num = len(text.split())
    # divide score by length
    score /= math.log(num)
    # return new score
    return score

# count cyber word frequency
def count_cyber_freq():
    # loop through text list
    for text in parse_text:
        # create cyber score
        score = 0
        # loop through glossary
        for term in glossary:
            format_term = " %s " % term
            # if term is present
            if format_term in text:
                # increase score
                score += calc_score(term)

        # adjust score depending on text length
        score = adjust_score(score, text)

        # print percent
        print("%s\n\n" % score)

clear_screen()
parse_files()
get_cyber_words()
word_freq()
count_cyber_freq()
