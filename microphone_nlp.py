import pyaudio as audio
import speech_recognition as sr
import nltk
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk import pos_tag
from nltk import RegexpParser

##############################
only_unique_words = True
###############33

# create a list of stopwords to ignore...
stopwords = set(['shan', 'same', "wasn't", "she's", 'they', 'off', "needn't", "weren't", 'as', 'some', 'and', 'from', 'other', "shouldn't", "shan't", 'to', 'does', 'was', 'has', 'so', 'himself', 'do', 'below', "doesn't", "that'll", 'its', 'these', 'are', 'more', 'aren', 'all', 'whom', 'shouldn', 'too', 'over', "you've", 'him', 'o', 'his', 'be', "you'll", 'out', 'against', 'most', 'if', 'hasn', 'own', 's', 'what', 'theirs', 'or', "it's", 'will', "don't", 'is', 'been', 'who', 'yourselves', 'her', 'did', 'the', 'up', 'there', 'ourselves', 'during', 'mightn', "you'd", 'further', 'very', 'those', 'for', 'but', 'an', 'in', 'nor', "mightn't", 've', 'both', 'until', 'isn', 'ain', "didn't", 'than', 'themselves', 'myself', "couldn't", 'now', 'herself', 'any', 'by', "wouldn't", 'about', 'after', 'here', 'doesn', 'a', 'which', 'd', 'y', 'were', 'couldn', "aren't", 'i', 'then', 'being', 'just', 'our', "haven't", 't', 'wouldn', 're', "mustn't", 'while', 'with', 'only', 'under', 'ma', 'again', 'can', 'ours', 'through', "hadn't", 'when', 'hers', "isn't", 'of', 'few', 'my', 'had', 'before', 'where', 'wasn', "should've", 'she', 'your', 'haven', 'weren', 'on', 'have', 'he', 'between', 'me', 'down', 'should', 'mustn', 'their', 'am', 'above', 'll', 'such', 'why', 'no', 'you', 'it', 'because', 'into', 'm', "you're", 'that', 'itself', 'not', 'hadn', "won't", 'we', 'don', 'doing', 'won', 'them', 'this', "hasn't", 'how', 'at', 'needn', 'once', 'having', 'yours', 'each', 'yourself', 'didn'])

print("stop_words: ", stopwords)

stemmer = PorterStemmer()

# create a queue of the last 100 words identified by the program
recent_text_q = []
max_q_len = 100

# activate macbook microphone stream
## figure out what audio device our microphone is
print(sr.Microphone.list_microphone_names())
index = 0

print("should be the internal microphone: ", sr.Microphone.list_microphone_names()[index])

# create a microphone object
internal_mic = sr.Microphone(device_index = index)
# create a speech recognition object
recognizer = sr.Recognizer()


nouns = []
verbs = []


def fifoIn(lst, val, max_len):
    # check if item needs to be removed
    if len(lst) >= max_len:
        lst.pop(0)
    lst.append(val)
    return lst

while(1):
    # capture audio from the microphone
    with internal_mic as source:
        # adjust for background noise to increase success rate
        recognizer.adjust_for_ambient_noise(source)
        # identify any spoken words in the audio
        print("Speech Recognizer Enabled");
        audio = recognizer.listen(source)
        print("audio exported from source")
        raw_string = "the the "
        try:
            raw_string = recognizer.recognize_google(audio)
        except:
            print(" .")

        print("{} of tokenized words returned from google: {}".format(type(raw_string), raw_string))
        # remove words from string

        words = raw_string.split()
        wn = len(words)
        # remove any words in the stopwords
        words = [i for i in words if i not in stopwords]
        print("{} words removed from stopwords".format(wn - len(words)))
        words = [i for i in words if i not in recent_text_q]
        print("{} words removed from priorwords".format(wn - len(words)))
        # append the word type to the word string, returnig a tuple (str, type)
        words_tags = pos_tag(words)
        # create a chunk grammar statement
        """
            According to the rule you created, your chunks:
            Start with an optional (?) determiner ('DT')
            Can have any number (*) of adjectives (JJ)
            End with a noun (<NN>)
        grammar = "NP: {<DT>?<JJ>*<NN>}"
        chunk_parser = RegexpParser(grammar)
        tree = chunk_parser.parse(words_tags)
        """
        # append spoken words to the running FIFO of all words
        for word in words:
            recent_text_q = fifoIn(recent_text_q, word, max_q_len)

        print("{} identified words: ".format(len(recent_text_q)),
              recent_text_q)

# classify words and add them to FIFO buffers

# print current FIFO buffers
