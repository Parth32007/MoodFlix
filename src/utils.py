import ast
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def convert(text):
    L = []

    for i in ast.literal_eval(text):
        L.append(i['name'])

    return L

def convert_cast(text):
    L = []

    counter = 0

    for i in ast.literal_eval(text):

        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break

    return L

def fetch_director(text):

    L = []

    for i in ast.literal_eval(text):

        if i['job'] == 'Director':
            L.append(i['name'])

    return L

def stem(text):
    words = []

    for word in text.split():
        words.append(ps.stem(word))

    return " ".join(words)