import pyaudio as audio
import speech_recognition as sr
import nltk
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.tag import pos_tag
from nltk import RegexpParser
from os import system
from sys import path
path.append('../stable_diffusion')
import image_generator_from_text as img_generator
import random
##############################
only_unique_words = True
###############

# Download the required datafiles for the NLTK pos_tag function
nltk.download('averaged_perceptron_tagger')

# create a list of stopwords to ignore...
stopwords = set(['shan', 'same', "wasn't", "she's", 
                 'they', 'off', "needn't", "weren't", 
                 'as', 'some', 'and', 'from', 'other', 
                 "shouldn't", "shan't", 'to', 'does', 
                 'was', 'has', 'so', 'himself', 'do', 
                 'below', "doesn't", "that'll", 'its', 
                 'these', 'are', 'more', 'aren', 'all', 
                 'whom', 'shouldn', 'too', 'over', "you've", 
                 'him', 'o', 'his', 'be', "you'll", 'out', 
                 'against', 'most', 'if', 'hasn', 'own', 
                 's', 'what', 'theirs', 'or', "it's", 
                 'will', "don't", 'is', 'been', 'who', 
                 'yourselves', 'her', 'did', 'the', 'up', 
                 'there', 'ourselves', 'during', 'mightn', 
                 "you'd", 'further', 'very', 'those', 'for', 
                 'but', 'an', 'in', 'nor', "mightn't", 've', 
                 'both', 'until', 'isn', 'ain', "didn't", 
                 'than', 'themselves', 'myself', "couldn't", 
                 'now', 'herself', 'any', 'by', "wouldn't", 
                 'about', 'after', 'here', 'doesn', 'a', 
                 'which', 'd', 'y', 'were', 'couldn', 
                 "aren't", 'i', 'then', 'being', 'just', 
                 'our', "haven't", 't', 'wouldn', 're', 
                 "mustn't", 'while', 'with', 'only', 
                 'under', 'ma', 'again', 'can', 'ours', 
                 'through', "hadn't", 'when', 'hers', 
                 "isn't", 'of', 'few', 'my', 'had', 
                 'before', 'where', 'wasn', "should've", 
                 'she', 'your', 'haven', 'weren', 'on', 
                 'have', 'he', 'between', 'me', 'down', 
                 'should', 'mustn', 'their', 'am', 'above', 
                 'll', 'such', 'why', 'no', 'you', 'it', 
                 'because', 'into', 'm', "you're", 'that', 
                 'itself', 'not', 'hadn', "won't", 'we', 
                 'don', 'doing', 'won', 'them', 'this', 
                 "hasn't", 'how', 'at', 'needn', 'once', 
                 'having', 'yours', 'each', 'yourself', 'didn'])

print("stop_words: ", stopwords)



################################################################
## figure out what audio device our microphone is
def getMacbookProMic():
    print(sr.Microphone.list_microphone_names())
    internal_macbook_name = "MacBook Pro Microphone"
    index = sr.Microphone.list_microphone_names().index(internal_macbook_name)

    print("should be the internal microphone: ", sr.Microphone.list_microphone_names()[index])

    # create a microphone object
    internal_mic = sr.Microphone(device_index = index)
    return internal_mic

def fifoInDict(lst, val, tag, max_len):
    # check if item needs to be removed
    if len(lst) >= max_len:
        lst.pop(0)
    # update the dictionary
    temp_dict = {'word': val, 'type': tag, 'freq': 1}
    lst.append(temp_dict)
    return lst

def fifoInLst(lst, val, max_len):
    # check if item needs to be removed
    if len(lst) >= max_len:
        lst.pop(0)
    # update the dictionary
    lst.append(val)
    return lst

def speechToText(mic, recognizer):
    """
    Input : mic = st.Microphone() object where an audio stream can be read
            recognizer = sr.Recognizer() object that takes in a audio clip and returns a list of words
    Output: words = list of words that are identified from words spoken into the microphone
    """
    # capture audio from the microphone
    with mic as source:
        # adjust for background noise to increase success rate
        recognizer.adjust_for_ambient_noise(source)
        # identify any spoken words in the audio
        print("Speech Recognizer Enabled");
        audio = recognizer.listen(source)
        print("audio exported from source")
        raw_string = ""
        try:
            raw_string = recognizer.recognize_google(audio)
        except:
            print(" .")

        print("{} of tokenized words returned from google: {}".format(type(raw_string), raw_string))
        # remove words from string

        return_str = raw_string.split()
        wn = len(return_str)
        # remove any words in the stopwords
        words = [i for i in return_str if i not in stopwords]
        print("{} words removed from stopwords".format(wn - len(words)))
        words = [i for i in return_str if i not in recent_text_q]
        print("{} words removed from priorwords".format(wn - len(words)))
        return words
    
def tagWords(words):
    """
    Use NLTK to tag a list of words and return a tuple (str, type)
    This function should be run before storing the words into memory so the program
    knows what part of speech the words belong and can construct sentences from those
    words accordingly
    """
    words_tags = pos_tag(words)
    print("words tagged: {}".format(words_tags))
    return words_tags

def addWordsToMemory(words, tags):
    """

    """
    # create a dict to place in the list of heard words
    # append spoken words to the running FIFO of all words
    for i in range(words):
        recent_text_q = fifoInDict(recent_text_q, words[i], tags[i], max_q_len)
        # if append to buffer according to type of grammer

    print("{} identified words: ".format(len(recent_text_q)),
            recent_text_q)
    return recent_text_q

# classify words and add them to FIFO buffers

# print current FIFO buffers

def getStrFromTuple(lst):
    r = ""
    for l in lst:
        r.join(l[0]).join(" ")
    return r

def getStrFromList(lst):
    print(lst)
    r = ""
    for i in range(len(lst)):
        print(i)
        r.join(lst[i]).join(" ")
        print(r)
    return r

def createWordDict(word_tags):
    word_dict = {}
    for word, pos in word_tags:
        if word in word_dict:
            word_dict[word]["freq"] += 1
        else:
            word_dict[word] = {"word": word, "type": pos, "freq": 1}

    consolidated_list = list(word_dict.values())
    return consolidated_list

    # keep listening until 50 words are heard and stored in memory
def listenForWords(min_words, max_words):
    new_words = []
    macbook_mic = getMacbookProMic()
    while len(new_words) < min_words:
        results = speechToText(macbook_mic, recognizer)
        if results is not []:
            new_words.extend(results)
            print("List of {} words includes: {}".format(len(new_words), new_words[:-5]))
        else:
            print("No words detected")
    return new_words[:max_words]

def populateGrammarLists(recent_text_q, nouns, verbs, adjectives):
    for word in recent_text_q:
        print("word : {}".format(word))
        if word['type'].startswith("NN"):
            for i in range(word['freq']):
                nouns = fifoInLst(nouns, word['word'], max_q_len)
        elif word['type'].startswith("VB"):
            for i in range(word['freq']):
                verbs = fifoInLst(verbs, word['word'], max_q_len)
        elif word['type'].startswith("JJ"):
            for i in range(word['freq']):
                adjectives = fifoInLst(adjectives, word['word'], max_q_len)
        prompt_string = ""
    return nouns, verbs, adjectives

def addSimplePhraise():
    # generate multiple phraises, then determine best one using nltk
    return "{} {} {} {} {}".format(randomNoun(), randomAdj(), randomNoun(), randomVerb(), randomNoun())

def randomNoun():
    return nouns[random.randint(0, len(nouns) - 1)]

def randomVerb():
    return verbs[random.randint(0, len(verbs) - 1)]

def randomAdj():
    return adjectives[random.randint(0, len(adjectives) - 1)]

def espeakPrompt(prompt):
    gender = 'm' # as oppose to  'f'
    vnum = str(random.randint(1, 5))
    voice = '{}{}'.format(gender, vnum)
    pitch = str(random.randint(10, 90))
    command = 'espeak -s 180 -v {} -p {} "{}"\n'.format(voice, pitch, prompt)
    print("using espeak to say the following command {}".format(prompt))
    system(command)

if __name__ == "__main__":
    stemmer = PorterStemmer()

    # create a queue of the last 100 words identified by the program
    # recent_text_q is a list of dicts with three values: word, type, and freq
    recent_text_q = []
    max_q_len = 100
    nouns = []
    verbs = []
    adjectives = []

    # activate macbook microphone stream
    # create a speech recognition object
    recognizer = sr.Recognizer()
    words = listenForWords(50, 100)
    print('we found a total of {} words: {}'.format(len(words), words))
    word_tags = tagWords(words)
    recent_text_q = createWordDict(word_tags)
    print(recent_text_q)

    nouns, verbs, adjectives = populateGrammarLists(recent_text_q, nouns, verbs, adjectives)
    print("{} nouns are saved: {}".format(len(nouns), nouns))
    print("{} verbs are saved: {}".format(len(verbs), verbs))
    print("{} adjectives are saved: {}".format(len(adjectives), adjectives))

    prompt_string = []
    prompt_string.append("Abstract painting in the cubist style of {}".format(addSimplePhraise()))
    prompt_string.append("Abstract painting in the expressionist style of {}".format(addSimplePhraise()))
    prompt_string.append("Abstract drawing in the cubist style of {}".format(addSimplePhraise()))
    
    print(prompt_string)
    espeakPrompt(prompt_string)

    arg_dict = {
    'output_width': 512,
    'output_height': 512,
    'prompts': prompt_string,
    'batch_size': 1,
    'steps' : 12,
    'seed' : 1290,
    'plot_output': True,
    'upscale': 2.0
    }
    print(arg_dict)
    img_generator.main(arg_dict)