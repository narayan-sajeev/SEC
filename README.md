# README for SEC 10-K Parsing Script

This Python script is designed to parse text from SEC 10-K filings and give each company a cybersecurity awareness score. 

## Dependencies
This script requires the following Python modules to be installed:

- `os`
- `beautifulsoup4`
- `string`
- `nltk`
- `urllib`
- `math`

## Usage
To use the script, follow these steps:

1. Install the required dependencies.
2. Place the SEC 10-K filings you wish to parse in a directory called `Files` located in the same directory as the script.
3. Run the script from the command line: `python parse.py`

## Functions
The script includes the following functions:

- `remove_substrings(text, substrings)`: removes substrings from a given text.
- `remove_whitespace(text)`: removes whitespace from a given text.
- `includes_digit(word, digits)`: checks if a given word includes a digit.
- `remove_num(text)`: removes numbers from a given text.
- `remove_stop_words(text)`: removes the most common English words from a given text.
- `parse_files()`: parses the SEC 10-K filings in the Files directory and generates a dictionary of parsed text for each company in the filings.
- `format_glossary(text)`: formats a given text for inclusion in the cybersecurity glossary.
- `return_possible_words(word)`: retrieves possible words from a given word with parentheses.
- `get_cyber_words()`: generates a glossary of cybersecurity terms from the SEC 10-K filings.
