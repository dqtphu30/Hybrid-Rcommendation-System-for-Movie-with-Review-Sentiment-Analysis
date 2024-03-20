import numpy as np
from collections import Counter, defaultdict
from nltk.tokenize import word_tokenize
from scipy.sparse import csr_matrix
from sentiment_analysis.preprocessing import processtext

class reviewTfidfVectorizer:
    def __init__(self, n_gram_range = (1,1)):
        """
        Initialize Vietnamese TF-IDF Vectorizer.

        Attributes:
        - vocabulary_: A dictionary mapping words to their indices in the vocabulary.
        - document_counts: A Counter object storing the document frequency of each word.
        - tf_idf_transformer: TfidfTransformer instance for transforming TF to TF-IDF.
        """
        
        self.vocabulary_ = {}
        self.document_counts = defaultdict(int)
        self.document_term_frequency = defaultdict(int)
        self.N = 0
        self.n_gram_range = n_gram_range

    def fit_transform(self, corpus):
        """
        Fit the vectorizer on the given corpus and transform it into a TF-IDF matrix.

        Parameters:
        - corpus: List of text documents.

        Returns:
        - tfidf_matrix: Sparse TF-IDF matrix representing the input corpus.
        """
        
        self.fit(corpus)
        return self.transform(corpus)

    def fit(self, corpus):
        """
        Fit the vectorizer on the given corpus.

        Parameters:
        - corpus: List of text documents.
        """
        self.N = len(corpus)
        tokenized_corpus = [self.tokenize(text) for text in corpus]
        print("Tokenized Corpus Successful!")
        self.document_counts = dict(Counter(word for tokens in tokenized_corpus for word in tokens))
        print("Document Count Successful!")
        vocal_filt = dict(filter(self.my_filtering_function, self.document_counts.items()))
        set_vocab = set(vocal_filt.keys())
        self.vocabulary_ = {word: idx for idx, word in enumerate(set_vocab)}
        print("Vocabulary Successful!")
        # Đếm số câu chứa từng từ trong từ vựng
        for tokens in tokenized_corpus:
            unique_tokens = set(tokens)
            for token in unique_tokens.intersection(self.vocabulary_):
                self.document_term_frequency[token] += 1
        print("Successful!")

    def transform(self, corpus):
        """
        Transform the given corpus into a TF-IDF matrix.

        Parameters:
        - corpus: List of text documents.

        Returns:
        - tfidf_matrix: Sparse TF-IDF matrix representing the input corpus.
        """
        
        n_vocab = len(self.vocabulary_)
        n_sents = len(corpus)
        rows = []
        cols = []
        data = []

        for i in range(n_sents):
            tokens = self.tokenize(corpus[i])
            for token in set(tokens):
                if token in self.vocabulary_:
                    term_frequency = np.log10(self.document_counts[token] + 1) 
                    idf = np.log10(self.N / self.document_term_frequency[token])
                    rows.append(i)
                    cols.append(self.vocabulary_[token])
                    data.append(term_frequency * idf)

        tfidf_matrix = csr_matrix((data, (rows, cols)), shape=(n_sents, n_vocab))
        return tfidf_matrix

    def tokenize(self, text):

        tokens = word_tokenize(self.processtext(text))
        
        # Generate n-grams
        n_grams = []
        min_n, max_n = self.n_gram_range
        for n in range(min_n, max_n + 1):
            if n == 1:
                n_grams.extend(tokens)  # Unigrams
            else:
                n_grams.extend(" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1))  # N-grams

        return n_grams
    
    def processtext(self, text):
        return processtext(text)

    def my_filtering_function(self, pair):
        key, value = pair
        if value >= 30:
            return True  # keep pair in the filtered dictionary
        else:
            return False  # filter pair out of the dictionary