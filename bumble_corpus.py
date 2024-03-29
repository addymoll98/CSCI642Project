from math import prod
import os, os.path
import string
import nltk, string, re
from nltk import FreqDist, NaiveBayesClassifier, classify
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus.reader import CategorizedPlaintextCorpusReader
import random
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from nltk.stem import WordNetLemmatizer

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
	punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
	for ele in text:
		if ele in punc:
			text = text.replace(ele, "")
	return text

bumble=CategorizedPlaintextCorpusReader('/Users/sohaibkhan/nltk_data/corpora/bumble',  \
                                 '.*', \
                                 cat_pattern=r'(.*)[/]')

#print(bumble.categories())

docs = []

lemmatizer = WordNetLemmatizer()
punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

def accronym(word):
	accronyms=[
		('app','application'),
		('bot','robot'),
		('bots','robots'),
		('vs','versus')
	]
	for acc in accronyms:
		x,y=acc
		if x==word:
			return y
	return ""

for category in bumble.categories():
	for fileid in bumble.fileids(category):
		if len(bumble.words(fileid)) > 9:
			docs.append((bumble.words(fileid), category))
			#documents.append((bumble.sents(fileid),category))

documents=[]

for doc in docs:
	x,y=doc
	documents.append((list(x),y))

for i in range(len(documents)):
	x,y=documents[i]
	for j in range(len(x)):
		word=x[j]
		if word in punc:
			word=''
		word=remove_emoji(word)
		word=word.lower()
		word=lemmatizer.lemmatize(word)
		if accronym(word)!='':
			word=accronym(word)
		x[j]=word
	documents[i]=(x,y)




stopwords_english = stopwords.words('english')
#print(stopwords_english)


cleaned_docs=[]

for i in range(len(documents)):
	x,y=documents[i]
	z=[]
	for word in x:
		if word not in stopwords_english and word!='':
			z.append(word)
			# x.remove(word)
		# 	if i==0:
		# 		print("removed ", word)
		# if word=='':
		# 	x.remove(word)
	documents[i]=(z,y)
	if i==0:
		print("printing z", z)



# print(documents[0])
# print(documents[300])

all_words_clean=[]
for document in documents:
	docx,docy=document
	for word in docx:
		all_words_clean.append(word)

all_words_frequency = FreqDist(all_words_clean)

most_common_words = all_words_frequency.most_common(2000)

word_features = [item[0] for item in most_common_words]

def document_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

feature_set = [(document_features(doc), category) for (doc, category) in documents]
random.shuffle(feature_set)

#print(feature_set[0][0])

train_set = feature_set[400:]
test_set = feature_set[:400]

NBclassifier = NaiveBayesClassifier.train(train_set)

#accuracy
accuracy = classify.accuracy(NBclassifier,test_set)
print(accuracy)

app_func=[]
app_func=[0 for i in range(3)]
cust_serv=[]
cust_serv=[0 for i in range(3)]
prod_sat=[]
prod_sat=[0 for i in range(3)]


y_true=[]
y_pred=[]

for document in test_set:
	x,y=document
	if y=="app_func":
		i=0
		y_true.append(0)
	elif y=="cust_serv":
		i=1
		y_true.append(1)
	elif y=="prod_sat":
		i=2
		y_true.append(2)
	this_class=NBclassifier.classify(x)
	if this_class=="app_func":
		app_func[i]=app_func[i]+1
		y_pred.append(0)
	elif this_class=="cust_serv":
		cust_serv[i]=cust_serv[i]+1
		y_pred.append(1)
	elif this_class=="prod_sat":
		prod_sat[i]=prod_sat[i]+1
		y_pred.append(2)

print(app_func)
print(cust_serv)
print(prod_sat)
target_names=['app_func', 'cust_serv', 'prod_sat']

print(classification_report(y_true,y_pred,target_names=target_names))

###########ALL this stuff below is trying to figure stuff out kinda stuff...

# X,y=make_classification(n_samples=1000, n_features=1, n_informative=0, n_redundant=0, n_repeated=0, n_classes=3)

# from sklearn.model_selection import train_test_split


# for document in feature_set:
# 	xd,yd=document
# 	X.append()

# X_train, X_test, y_train,y_test=train_test_split(X, y, test_size=.4)

# from sklearn.svm import SVC
# from sklearn.metrics import accuracy_score

# clf=SVC(gamma='auto')
# clf.fit(X_train,y_train)
# y_pred=clf.predict(X_test)
# print(accuracy_score(y_test,y_pred))

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import SVC
from sklearn import model_selection

from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation

#SVC model training and accuracy
model_svc = SklearnClassifier(SVC(kernel = 'linear'))
model_svc.train(train_set)


svc_accuracy = nltk.classify.accuracy(model_svc, test_set)
print('SVC Accuracy : ',svc_accuracy)
print()


#Decision Tree model training and accuracy


# model_tree = SklearnClassifier(DecisionTreeClassifier(kernel = 'linear'))
# model_tree.train(train_set)
# tree_accuracy = nltk.classify.accuracy(model_tree, test_set)

# Create Decision Tree classifer object
# clf = DecisionTreeClassifier()

# # Train Decision Tree Classifer
# clf = clf.fit(train_set)

# #Predict the response for test dataset
# y_pred = clf.predict(test_set)

# tree_accuracy = metrics.accuracy_score(train_set, y_pred)
# print('Decision tree accuracy: ')

###All this is balancing the data

balanced_feature_set=feature_set

app_func=0
cust_serv=0
prod_sat=0
for member in balanced_feature_set:
	x,y=member
	if y=="app_func":
		app_func+=1
	elif y=="cust_serv":
		cust_serv+=1
	elif y=="prod_sat":
		prod_sat+=1

while app_func < prod_sat and cust_serv<prod_sat:
	for member in balanced_feature_set:
		x,y=member
		if y=="app_func":
			if app_func < prod_sat:
				balanced_feature_set.append((x,y))
				app_func+=1
		elif y=="cust_serv":
			if cust_serv < prod_sat:
				balanced_feature_set.append((x,y))
				cust_serv+=1

random.shuffle(balanced_feature_set)

balanced_train_set = balanced_feature_set[400:]
balanced_test_set = balanced_feature_set[:400]

NBclassifier = NaiveBayesClassifier.train(balanced_train_set)

#accuracy
accuracy = classify.accuracy(NBclassifier,balanced_test_set)
print(accuracy)

app_func=[]
app_func=[0 for i in range(3)]
cust_serv=[]
cust_serv=[0 for i in range(3)]
prod_sat=[]
prod_sat=[0 for i in range(3)]


y_true=[]
y_pred=[]

for document in balanced_test_set:
	x,y=document
	if y=="app_func":
		i=0
		y_true.append(0)
	elif y=="cust_serv":
		i=1
		y_true.append(1)
	elif y=="prod_sat":
		i=2
		y_true.append(2)
	this_class=NBclassifier.classify(x)
	if this_class=="app_func":
		app_func[i]=app_func[i]+1
		y_pred.append(0)
	elif this_class=="cust_serv":
		cust_serv[i]=cust_serv[i]+1
		y_pred.append(1)
	elif this_class=="prod_sat":
		prod_sat[i]=prod_sat[i]+1
		y_pred.append(2)

print(app_func)
print(cust_serv)
print(prod_sat)
target_names=['app_func', 'cust_serv', 'prod_sat']

