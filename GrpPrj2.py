import string
import re
import pathlib

arr = []  

def browse_inputfile(file):
    with open (file, 'r') as f:
        contents = f.readlines()
        for word in contents:
            word = word.split()
            for letter in word:
                if len(letter) == 3:
                    if letter not in arr:
                        arr.append(letter)
    return 

for path in pathlib.Path("/Users/tobennaeze/Downloads/prod_sat").iterdir():
    if path.is_file():
        current_file = path
        browse_inputfile(current_file)        

print (arr)