#!/usr/bin/env python3

import nltk
import csv
from nltk.util import bigrams, trigrams 
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer # Add Lemmatizer!!!
import pickle

# Open 'item_list' containing yelp reviews
with open("items.csv") as file:
    reader = csv.reader(file)
    item_list = list(reader)
item_list = item_list[1:]

all_words = []
allowed_word_types = ["JJ","RB","MD"]

all_bigrams = []

# Create lemmatizer
lemmatizer = WordNetLemmatizer()

# Tokenize by word, bigram, and trigram... add desired word types to corresponding lists 
for item in item_list:
    
    words = word_tokenize(str(item))
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][:2] in allowed_word_types:
            wLemma = lemmatizer.lemmatize(w[0])
            all_words.append(wLemma.lower())
    
    bgrams = bigrams(words)
    for b in bgrams:

        w0 = nltk.pos_tag(word_tokenize(b[0]))
        w1 = nltk.pos_tag(word_tokenize(b[1]))

        pos0 = [w[1] for w in w0][0][:2]
        pos1 = [w[1] for w in w1][0][:2]

        if (pos0 in allowed_word_types) or (pos1 in allowed_word_types):
            wlemma0 = lemmatizer.lemmatize(word_tokenize(b[0])[0]).lower()
            wlemma1 = lemmatizer.lemmatize(word_tokenize(b[1])[0]).lower()
            lemmatuple = []
            lemmatuple.append(str(wlemma0))
            lemmatuple.append(str(wlemma1))
            blemma = bigrams(lemmatuple)
            for _b in blemma:
                all_bigrams.append(_b)
            
 
# Create frequency distributions for words and bigrams
all_words = nltk.FreqDist(all_words)
all_bigrams = nltk.FreqDist(all_bigrams)

# Create word and bigram feature lists
word_feats = [i[0] for i in all_words.most_common(2500)]
bigram_feats = [i[0] for i in all_bigrams.most_common(500)]

#word_feats = list(all_words.keys())[:2500]
#bigram_feats = list(all_bigrams.keys())[:500]

all_feats = word_feats + bigram_feats 

# Save feature lists
save_word_feats = open("word_feats.pickle","wb")
pickle.dump(word_feats,save_word_feats)
save_word_feats.close()

save_bigram_feats = open("bigram_feats.pickle","wb")
pickle.dump(bigram_feats,save_bigram_feats)
save_bigram_feats.close()

save_all_feats = open("all_feats.pickle","wb")
pickle.dump(all_feats,save_all_feats)
save_all_feats.close()

# Freq feature set instead of presence feature set
# Should I lemmatize words before checking if in word feats??
def find_feats(review):
    words = word_tokenize(str(review))
    bgrams = bigrams(words)
    feats = []
    for wf in word_feats:
        freq = 0
        for w in words:
            wlemma = lemmatizer.lemmatize(w).lower()
            if wlemma == wf:
                freq += 1
        feats.append(float(freq)/float(len(words))) 
    for bf in bigram_feats:
        freq = 0
        for b in bgrams:
            wlemma0 = lemmatizer.lemmatize(word_tokenize(b[0])[0]).lower()
            wlemma1 = lemmatizer.lemmatize(word_tokenize(b[1])[0]).lower()
            lemmatuple = []
            lemmatuple.append(str(wlemma0))
            lemmatuple.append(str(wlemma1))
            blemma = bigrams(lemmatuple)
            for _b in blemma:
                if _b == bf:
                    freq += 1
        feats.append(float(freq)/float(len(words)))
    return feats

# Create feature sets
featsets = [find_feats(item) for item in item_list]


# Save feature sets
save_featsets = open("featsets.pickle","wb")
pickle.dump(featsets,save_featsets)
save_featsets.close()