from sec_edgar_downloader import Downloader
import os
import shutil
from bs4 import BeautifulSoup
import string

# create downloader object
download = Downloader()

# define companies to download
companies = ["AAPL", "MSFT", "TWTR"]

# define list of text to parse
parse_text = []

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
        pass

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
    # loop through substrings
    for s in substrings:
        # remove substring
        text = "".join(text.split(s))

    # return text
    return text

# remove whitespace from text
def remove_whitespace(text, whitespaces):

    # remove whitespace
    text = text.strip()

    # loop through whitespaces
    for w in whitespaces:
        # remove whitespace
        text = " ".join(text.split(w))

    # return text
    return text

# remove numbers from text
def remove_num(text):

    # define digits
    digits = list(string.digits)

    # define new text
    new_text = text.split()

    # loop through words
    for w in new_text:
        # loop through characters
        for c in w:
            # if character is a digit
            if c in digits:
                # remove word
                new_text.remove(w)
                # break out of loop
                break

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

            # remove punctuation and symbols from text
            formatted = remove_substrings(soup.text, ["\n", " | 2021 form 10-k | ", ".", ",", "’", ";"])

            # remove whitespace
            formatted = remove_whitespace(formatted, ["       ", "   "])

            # remove numbers
            formatted = remove_num(formatted)

            # add text to list
            parse_text.append(formatted)

clear_screen()
# create_dir()
# download_files()
# move_files()
# clean_files()
open_files()
