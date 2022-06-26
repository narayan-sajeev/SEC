from sec_edgar_downloader import Downloader
import os
import shutil

# create downloader object
download = Downloader()

# define file to download
file = "10-K"
# define companies to download
companies = ["AAPL", "MSFT", "TWTR"]
# define number of files per company
num_files = 1
# set parent directory of new folder to current directory
parent_dir = os.getcwd()
# define new directory (folder) name
new_dir = file + "_Files"

# define directory name
path = os.path.join(parent_dir, new_dir)

# try
try:
    # create directory
    os.mkdir(path)
# if directory already exists:
except:
    # do nothing
    pass

# loop through companies
for c in companies:
    # download company file
    download.get(file, c, amount=num_files)
