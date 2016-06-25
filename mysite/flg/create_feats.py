#!/usr/bin/env python3

import nltk
import csv
from nltk.util import bigrams, trigrams 
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from math import log
from operator import truediv
from joblib import Parallel, delayed
import pickle

# Open 'item_list' containing yelp reviews
with open("items.csv") as file:
    reader = csv.reader(file)
    item_list = list(reader)
item_list = item_list[1:]

all_words = []
all_bigrams = []
all_trigrams = []

allowed_types = ["JJ","RB","MD"]  # Adjectives and adverbs (maybe modals?)
bad_types = ['.', ',', ':', '"', '(', ')']

# Create lemmatizer
lemmatizer = WordNetLemmatizer()

# Tokenize by word, bigram, and trigram... add desired word types to corresponding lists 
for item in item_list:
    
    words = word_tokenize(str(item))
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][:2] in allowed_types and w[1][:2] not in bad_types:
            wLemma = lemmatizer.lemmatize(w[0])
            all_words.append(wLemma.lower())
    
    bgrams = bigrams(words)
    for b in bgrams:

        w0 = nltk.pos_tag(word_tokenize(b[0]))
        w1 = nltk.pos_tag(word_tokenize(b[1]))

        pos0 = [w[1] for w in w0][0][:2]
        pos1 = [w[1] for w in w1][0][:2]

        if (pos0 in allowed_types) or (pos1 in allowed_types):
            if (pos0 not in bad_types) and (pos1 not in bad_types):
                wlemma0 = lemmatizer.lemmatize(word_tokenize(b[0])[0]).lower()
                wlemma1 = lemmatizer.lemmatize(word_tokenize(b[1])[0]).lower()
                blemma = (str(wlemma0), str(wlemma1))
                all_bigrams.append(blemma)

    tgrams = trigrams(words)
    for t in tgrams:

        w0 = nltk.pos_tag(word_tokenize(t[0]))
        w1 = nltk.pos_tag(word_tokenize(t[1]))
        w2 = nltk.pos_tag(word_tokenize(t[2]))

        pos0 = [w[1] for w in w0][0][:2]
        pos1 = [w[1] for w in w1][0][:2]
        pos2 = [w[1] for w in w2][0][:2]

        if (pos0 in allowed_types) or (pos1 in allowed_types) or (pos2 in allowed_types):
            if (pos0 not in bad_types) and (pos1 not in bad_types) and (pos2 not in bad_types):
                wlemma0 = lemmatizer.lemmatize(word_tokenize(t[0])[0]).lower()
                wlemma1 = lemmatizer.lemmatize(word_tokenize(t[1])[0]).lower()
                wlemma2 = lemmatizer.lemmatize(word_tokenize(t[2])[0]).lower()
                tlemma = (str(wlemma0), str(wlemma1), str(wlemma2))
                all_trigrams.append(tlemma)

# Create frequency distributions for words and bigrams
all_words = nltk.FreqDist(all_words)
all_bigrams = nltk.FreqDist(all_bigrams)
all_trigrams = nltk.FreqDist(all_trigrams)

# Create word and bigram feature lists
word_feats = [i[0] for i in all_words.most_common(2500)]
bigram_feats = [i[0] for i in all_bigrams.most_common(450)]
trigram_feats = [i[0] for i in all_trigrams.most_common(50)]

all_feats = word_feats + bigram_feats + trigram_feats

# Save feature lists
save_word_feats = open("word_feats.pickle","wb")
pickle.dump(word_feats,save_word_feats)
save_word_feats.close()

save_bigram_feats = open("bigram_feats.pickle","wb")
pickle.dump(bigram_feats,save_bigram_feats)
save_bigram_feats.close()

save_trigram_feats = open("trigram_feats.pickle", "wb")
pickle.dump(trigram_feats, save_trigram_feats)
save_trigram_feats.close()

save_all_feats = open("all_feats.pickle","wb")
pickle.dump(all_feats,save_all_feats)
save_all_feats.close()

# Freq feature set instead of presence feature set
def find_feats(review):

    feats = []

    words = word_tokenize(str(review))
    wlemmas = [lemmatizer.lemmatize(w).lower() for w in words]
    for wf in word_feats:
        freq = 0
        for wl in wlemmas:
            if wl == wf:
                freq += 1
        feats.append(freq)

    bgrams = bigrams(words)
    blemmas = []
    for b in bgrams:
        wlemma0 = lemmatizer.lemmatize(word_tokenize(b[0])[0]).lower()
        wlemma1 = lemmatizer.lemmatize(word_tokenize(b[1])[0]).lower()
        blemma = (str(wlemma0), str(wlemma1))
        blemmas.append(blemma)
    for bf in bigram_feats:
        freq = 0
        for bl in blemmas:
            if bl == bf:
                freq += 1
        feats.append(freq)

    tgrams = trigrams(words)
    tlemmas = []
    for t in tgrams:
        wlemma0 = lemmatizer.lemmatize(word_tokenize(t[0])[0]).lower()
        wlemma1 = lemmatizer.lemmatize(word_tokenize(t[1])[0]).lower()
        wlemma2 = lemmatizer.lemmatize(word_tokenize(t[2])[0]).lower()
        tlemma = (str(wlemma0), str(wlemma1), str(wlemma2))
        tlemmas.append(tlemma)
    for tf in trigram_feats:
        freq = 0
        for tl in tlemmas:
            if tl == tf:
                freq += 1
        feats.append(freq)

    return feats

def TFIDF(feat):
    docnum = 0
    for fset in featsets:
        if fset[feat] > 0:
            docnum += 1
    inv_docfreq = log(docnum)
    for idx, fset in enumerate(featsets):
        featsets[idx][feat] = float(fset[feat] / inv_docfreq)

# Create feature sets
# featsets = Parallel(n_jobs=-1)(delayed(find_feats)(item) for item in item_list)
featsets = [find_feats(item) for item in item_list]

# TFIDF
# Parallel(n_jobs=-1)(delayed(TFIDF)(feat) for feat in range(len(all_feats)))
for feat in range(len(all_feats)):
    TFIDF(feat)

# Save feature sets
save_featsets = open("featsets.pickle","wb")
pickle.dump(featsets,save_featsets)
save_featsets.close()