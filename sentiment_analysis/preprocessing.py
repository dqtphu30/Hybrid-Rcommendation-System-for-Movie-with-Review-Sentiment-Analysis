from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re
import nltk
import en_core_web_sm

# Get stopwords
with open("sentiment_analysis/stopwords.txt", "r", encoding="utf-8") as file:
    stopwords = file.read().split("\n")
stopwords = set(stopwords)

nlp = en_core_web_sm.load()

lemmatizer=WordNetLemmatizer() 

def Name_Entity_Recognize(text):
    doc = nlp(text)
    ent = [(X, X.ent_iob_, X.ent_type_) for X in doc]
    temp = [i[0] for i in ent if i[2] in ['PERSON', 'DATE', 'ORG', 'GPE']]
    ner = []
    for i in temp:
        i = str(i)
        i = i.lower()
        ner.append(i)
    return ner

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def processtext(text):
    ner = Name_Entity_Recognize(text)
    # Remove HTML special entities (e.g. &amp;)
    text = re.sub(r'\&\w*;', '', text)
    #Convert @username to AT_USER
    text = re.sub('@[^\s]+','',text)
    # Remove tickers
    text = re.sub(r'\$\w*', '', text)
    # To lowercase
    text = text.lower()
    # Remove hyperlinks
    text = re.sub(r'https?:\/\/.*\/\w*', '', text)
    # Remove hashtags
    text = re.sub(r'#\w*', '', text)
    # Remove Punctuation
    text = re.sub(r'[^a-z0-9 ]+', ' ', text)
    # Remove whitespace (including new line characters)
    text = re.sub(r'\s\s+', ' ', text)
    # Remove digit
    text = re.sub(r'\b\d+\b', ' ', text)
    # Remove words with 2 or fewer letters
    text = re.sub(r'\b\w{1,2}\b', '', text)
    # Remove single space remaining at the front of the text.
    text = text.split()
    text = [w for w in text if w not in stopwords]
    # Xóa bỏ tên thực thể
    text = [w for w in text if w not in ner]
    # Xóa bỏ các hậu tố
    pos_tokens = nltk.pos_tag(text)
    text = [lemmatizer.lemmatize(pos[0], get_wordnet_pos(pos[1])) for pos in pos_tokens]
    # Remove characters beyond Basic Multilingual Plane (BMP) of Unicode:
    text = ' '.join(c for c in text if c <= '\uFFFF')
    return text

def readData(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    sentences = sent_tokenize(text)
    return sentences

def tokenizeWords(sentences):
    words = [word_tokenize(processtext(sentence)) for sentence in sentences]
    return words