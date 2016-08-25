from string import punctuation
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import Counter
from math import sqrt

numstr = '0123456789'

def tokenize(text):
    lower = text.lower()
    punct_free = lower.translate(str.maketrans(
        {key: None for key in punctuation}))
    punct_num_free = punct_free.translate(str.maketrans(
        {key: None for key in numstr}))
    tokens = word_tokenize(punct_num_free)
    porter = PorterStemmer()
    stemmed = [porter.stem(w) for w in tokens]
    tokens = [w for w in stemmed if w not in stopwords.words('english')]
    return Counter(tokens)


def cosineSimilairty(txt1, txt2):
    vec1 = Counter(tokenize(txt1))
    vec2 = Counter(tokenize(txt2))
    intersection = set(vec1.keys()) & set(vec2.keys())

    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominatior = sqrt(sum1) * sqrt(sum2)

    if not denominatior:
        return 0.0
    else:
        return float(numerator / denominatior)






