
import collections
import re
import random

to_ignore_char = {'$', ',', '.', ':', ';', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\\', '`', '\'', '+', '-',
                 '*', '/', '<', '>', '^', '%', '=', '?', '!', '(', ')', '[', ']', '{', '}', '_', '"', '&', '~', '@'}

to_ignore_word = {'$', ',', ':', ';', '0', '\\', '`', '\'', '+',
                 '*', '<', '>', '^', '%', '=', '?', '!', '(', ')', '[', ']', '{', '}', '_', '"', '&', '~'}



def normalize_text(text, ignored_chars):
    text = text.lower()
    for pattern in ignored_chars:
        text = re.sub(re.escape(pattern), '', text)
    text = re.sub('#.*', '', text)
    text = re.sub(re.escape('.'), ' . ', text)
    return text


def ngram_char_set(text, n=4):
    all = set()
    for string in normalize_text(text, to_ignore_char).split():
        chars = list(string)
        for i in range(len(chars) - n + 1):
            all.add(tuple(chars[i: i+n]))
    return all


def ngram_word_set(text, n=4):
    all = set()
    words = normalize_text(text, to_ignore_word).split()
    for i in range(len(words) - n + 1):
        all.add(tuple(words[i: i+n]))
    return all


def markov_chain(ngrams):
    chain = collections.defaultdict(list)
    for ngram in ngrams:
        chain[ngram[:-1]].append(ngram[-1])
    return chain


def random_sample(markov, max_size, separator, n=4):
    text = ''
    for el in random.choice(markov.keys()):
        text = text + separator + el
    for i in range(max_size):
        if separator == '':
            rand = random.choice(markov[tuple(text[-(n-1):])]) if markov[tuple(text[-(n-1):])] != [] else ''
        else:
            rand = random.choice(markov[tuple(text.split(separator)[-(n-1):])]) if markov[tuple(text.split()[-(n-1):])] != [] else ''
        text = text + separator + rand
    return text

with open("data/formy_utf.txt") as file:
    formy = file.read()
with open("data/pap.txt") as file:
    pap = file.read()

char_markov_chain = markov_chain(ngram_char_set(formy))
word_markov_chain = markov_chain(ngram_word_set(pap))

print(1)
print(random_sample(char_markov_chain, 6, ''))
print(2)
info = random_sample(word_markov_chain, 100, ' ').split(".")[1:-1]
for line in info:
    print(line)



