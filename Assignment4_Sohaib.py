import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, movie_reviews

#Open the test data txt file and store it in data variable
f = open('Testdatafile.txt', 'r')
data = f.read()
f.close()


#Since nltk expects a key field after words, this function removes all the stop words and adds the True key after each word
def create_word_features(words):
    useful_words = [word for word in words if word not in stopwords.words("english")]
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict

#Creating a list for all the negative reviews from movie_reviews and
# passing it through the create_words_feature function to remove stopwords
neg_reviews = []
for fileid in movie_reviews.fileids('neg'):
    words = movie_reviews.words(fileid)
    neg_reviews.append((create_word_features(words), "negative"))


#Creating a list for all the positive reviews from movie_reviews and 
# passing it through the create_words_feature function to remove stopwords
pos_reviews = []
for fileid in movie_reviews.fileids('pos'):
    words = movie_reviews.words(fileid)
    pos_reviews.append((create_word_features(words), "positive"))



#Creating the training set of 2000 reviews and test data sets of 500 reviews
train_set = neg_reviews[:1000] + pos_reviews[:1000]
test_set =  neg_reviews[750:] + pos_reviews[750:]

#Training the model with the naive bayes classifier
classifier = NaiveBayesClassifier.train(train_set)

#Printing the accuracy
accuracy = nltk.classify.util.accuracy(classifier, test_set)
print("The accuracy of the trained model is: ", accuracy * 100)


#Classifying the test data file txt using the trained classifier
words = word_tokenize(data)
words = create_word_features(words)
print("The class category of the test data file is: ", classifier.classify(words))







