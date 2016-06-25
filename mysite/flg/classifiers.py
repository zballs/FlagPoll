#!/usr/bin/env python3

import pickle
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

# Retrieve feature sets
open_featsets = open("featsets.pickle","rb")
featsets = pickle.load(open_featsets)
open_featsets.close()

# Retrieve non-text content used for classification
open_ratings = open("ratings.pickle","rb")
ratings = pickle.load(open_ratings)
open_ratings.close()

if len(featsets) != len(ratings):
	print("Number of featsets does not equal number of ratings")

# sklearn classifiers
gnb = GaussianNB()
gnb.fit(featsets,ratings)

knn = KNeighborsClassifier()
knn.fit(featsets,ratings)

svc = SVC()
svc.fit(featsets,ratings)

# Save supervised classifiers 
save_gnb = open("gnb.pickle","wb")
pickle.dump(gnb,save_gnb)
save_gnb.close()

save_knn = open("knn.pickle","wb")
pickle.dump(knn,save_knn)
save_knn.close()

save_svc = open("svc.pickle","wb")
pickle.dump(svc,save_svc)
save_svc.close()