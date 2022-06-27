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

# create downloader object
download = Downloader()

# define companies to download
companies = ["AAPL", "MSFT", "TWTR"]

# define list of text to parse
parse_text = []

# define list to store word counts
count_lst = []

# clear screen
def clear_screen():
    # repeat 4 times
    for i in range(4):
        # clear screen
        os.system("clear")

# create directory (folder) to store files
def create_dir():

    # set parent directory of new folder to current directory
    parent_dir = os.getcwd()

    # define new directory name
    path = os.path.join(parent_dir, "Files")

    # try
    try:
        # create directory
        os.mkdir(path)
    # if directory already exists:
    except:
        # do nothing
        pass

# download 10-K files
def download_files():
    # loop through companies
    for comp in companies:
        # download company file
        download.get("10-K", comp, amount=1)

# move files from nested directories to unified directory
def move_files():
    # loop through company folder
    for comp in os.listdir("sec-edgar-filings"):

        # if directory starts with "."
        if comp.startswith("."):
            # invalid, go to next directory
            continue
        # define company directory name
        comp_dir = os.path.join("sec-edgar-filings", comp)
        # define file directory name
        f_dir = os.path.join(comp_dir, "10-K")

        # loop through directories
        for dir in os.listdir(f_dir):

            # if directory starts with "."
            if dir.startswith("."):
                # invalid, go to next directory
                continue

            # define current directory
            curr_dir = os.path.join(f_dir, dir)
            # define current path
            curr_path = os.path.join(curr_dir, "filing-details.html")

            # define new filename
            new_fname = comp + ".html"
            # define new path
            new_path = os.path.join("Files", new_fname)

            # move file from old directory to new directory
            shutil.move(curr_path, new_path)

# clean code in files
def clean_files():
    # for filename in directory
    for fname in os.listdir("Files"):

        # if filename starts with "."
        if fname.startswith("."):
            # invalid, go to next file
            continue

        # define path
        path = os.path.join("Files", fname)

        # create string to hold cleaned file text
        cleaned_file = ""

        # open file to read
        with open(path, "r") as file:
            # read file
            text = file.read()
            # reduce newlines
            text = text.strip()

            # define formatted string
            formatted = ""

            # loop through characters
            for c in text:
                # if character is non-breaking space
                if ord(c) == 160:
                    # replace with standard space
                    formatted += " "
                # otherwise
                else:
                    # add character to string
                    formatted += c

            # use beautiful soup
            soup = BeautifulSoup(formatted, "html.parser")
            # clean code
            cleaned_file = soup.prettify()

        # open file to write
        with open(path, "w") as old_file:
            # replace file with cleaned file
            old_file.write(cleaned_file)

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
def includes(word, digits):
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
        if not includes(w, digits):
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

# open files
def open_files():
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

# find word counts
def word_count():

    # loop through text
    for text in parse_text:
        # define counter
        counter = {}
        # loop through words
        for word in text.split():
            # increment word count
            counter[word] = counter.get(word, 0) + 1

        # retrieve keys
        keys = list(counter.keys())

        # sort keys
        keys.sort()

        # loop through words
        for i, word in enumerate(keys):
            # if it is not last word
            if i + 1 < len(keys):
                # retrieve next word
                next_word = keys[i + 1]
                # check if next word contains this word and if next word is not much larger (not another word entirely)
                if word in next_word and len(next_word) - len(word) < 3:
                    # update word count of next word
                    counter[next_word] = counter.get(next_word, 0) + counter.get(word, 0)
                    # remove current word
                    counter.pop(word)

        # define current list
        curr_lst = []

        # loop through counts
        for word, freq in counter.items():
            # add count to list
            curr_lst.append([freq, word])

        # sort list in descending order
        curr_lst.sort(reverse=True)

        # add current list to list of lists
        count_lst.append(curr_lst)

    # loop through list of lists
    for lst in count_lst:
        # loop through list
        for freq, word in lst:
            # print word and frequency
            print("%s: %s\n\n\n" % (word, freq))

clear_screen()
# create_dir()
# download_files()
# move_files()
# clean_files()
open_files()
word_count()
