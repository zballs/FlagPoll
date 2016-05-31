import pickle
import datetime
from pll.models import Voice 
# from agg_clust import AgglomerativeClustering, Classify, Merge
import clust_mod
from clust_mod import whichCluster

tags = ('admin','buildings','community','education','events','sustainability','health','parks','safety','sanitation','transportation','other')

# Get today and date 30 days ago
today = datetime.date.today()
trailing30 = today - datetime.timedelta(days=30)

# Create comment and text dictionaries
comments = {}
text = {}
for t in tags:
    comments[t] = []
    text[t] = ''

# Create categorytext list and empty sentiment ledger 
categorytext = []
ledger = {}

# Get voices from trailing 30 days
voices = Voice.objects.filter(pub_date >= trailing30).order_by('-pub_date')


# Sort comments by category tag
for t in tags:
    for v in voices:
        response = str(v.opinion)
        updown = v.updown_votes
        polltag = v.question.tag
        if polltag == t:
            comments[t].append(v)
            text[t] += response
            for _ in range(updown-1):
                text[t] += response
    categorytext.append(t, text[t]) 


# Sentiment classification and labels for each category
for t in tags:
    category_text = text[t]
    clust, labels = whichCluster(category_text)
    ledger[t] = labels

save_ledger = open("ledger.pickle","wb")
pickle.dump(ledger, save_ledger)
save_ledger.close()


# Run web application on govt/organization server, database containing user information, polls, comments, and other content
# "Export" app content to blockchain/decentralized system
# Constituent nodes execute training and testing procedures for sentiment analysis
# ***Training - constituent node creates featuresets for random training set of yelp reviews, implements clustering method with featuresets
# ***Testing - constituent node uses clustering (developed by other constituent node in training?) to classify category sentiment (w cluster labels) in ledger
# What's the benefit of having constituent nodes in a decentralized network run the training and testing procedures for the sentiment analysis process?
#   1) Training especially takes a long time, sifting through tens of thousands of Yelp reviews and finding word/bigram features and feature frequencies
#      Having users execute these scripts on the blockchain takes the computational burden off the admin hosting the application on a server
#   2) Enabling constituent nodes to run the procedures allows for a multiplicity of clustering implementations, resulting from different parameters, input variables, (i.e. user options to-be-determined)
#      and stochastic operations involved in the clustering algorithm. Conmmonalities in user-generated category sentiment classifications via selection of cluster labels may elucidate the actual character
#      and causality of category sentiment, while discrepancies may allow local officials and constituents to separate noise.
#   3) 
#
# Aggregation & Synthesis - ledger archived in master ledger, which synthesizes all node ledgers into a summative set of category measures
# Explanation - Why is label X in the master ledger? Constituent nodes can send explanations or criticisms of category sentiment classifcation labels... these "logs" are archived in a master log
# Suggestions for improvements - 

# Alternatives
# Constituent nodes compete to solve proof-of-work puzzles and log computed ledgers in master ledger

# Constituent nodes execute smart contracts, each of which corresponds to a component procedure in the sentiment analysis process
# CREATE training set from corpus of yelp reviews and CONSTRUCT feature sets for each review in the training set
# COMMUNICATE with other consituent nodes, sending/receiving feature sets constructed in the previous step
# CLUSTR feature sets, constructed or received from another node, performing one iteration of contested agglomerging
# CONCRETIZE clustering upon completion
# CLASSIFY comment text blocks with completed clustering 






# Code for loading/saving comments, text, and date

# try:
#     Comments = open("comments.pickle","rb")
#     loaded_comments = pickle.load(Comments)
#     Comments.close()

#     Text = open("text.pickle","rb")
#     loaded_text = pickle.load(Text)
#     Text.close()

#     Date = open("date.pickle","rb")
#     date_last = pickle.load(Date)
#     Date.close()

# except:
#     loaded_comments = None
#     date_last = None

# Create comments dictionary if no loaded comments
# if not loaded_comments: 

# Create comments dictionary if new month/year
# if date_last:
#     if (today.month != date_last.month or today.year != date_last.year):
#         comments = {}
#         text = {}
#         for t in tags:
#             comments[t] = []
#             text[t] = ''

# Get all comments from this month
 # voices = Voice.objects.filter(pub_date__year=today.year, pub_date__month=today.month).order_by('-pub_date')

# Get comments from trailing 30 days

# if loaded_comments:
#     if today.month == date_last.month and today.year == date_last.year:
#         for cat in loaded_comments:
#             for com in loaded_comments[cat]:
#                 if com in voices:
#                     voices.remove(com)
#         for t in tags:
#             for v in voices:
#                 response = str(v.opinion)
#                 polltag = v.question.tag
#                 if polltag == t:
#                     loaded_comments[t].append(v)
#                     loaded_text[t] += response

#         comments = loaded_comments
#         text = loaded_text

# else:

# save_comments = open("comments.pickle","wb")
# pickle.dump(comments, save_comments)
# save_comments.close()

# save_text = open("text.pickle","wb")
# pickle.dump(text, save_text)
# save_text.close()

# save_date = open("date.pickle","wb")
# pickle.dump(today, save_date)
# save_date.close()
