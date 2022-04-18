import pandas as pd
import csv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import re

def remove_emoji(text):
    emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002700-\U000027BF"  # Dingbats
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text) 
def remove_punc(text):
    table = str.maketrans("", "", string.punctuation)
    return text.translate(table)

def remove_stopwords(text):
    text = word_tokenize(text)
    text_without_sw = [word for word in text if not word in stopwords.words()]
    return " ".join(text_without_sw)


