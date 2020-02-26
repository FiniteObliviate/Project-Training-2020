
# Exercise1: Write a Python code to count the words in this readme.
# Edited by Zhang Yedi on 2020/2/26


import re
def count_word(f):
    with open(f) as file:
        text = file.read()
        word = re.findall(r'[a-zA-Z]+', text)
        count = len(word)
    return count

