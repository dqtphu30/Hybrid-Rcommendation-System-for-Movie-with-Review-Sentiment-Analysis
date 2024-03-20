from sentiment_analysis.preprocessing import readData, tokenizeWords
from w2v import movieFeedbackWord2Vec

def createW2VModel(models = ["skipgram"]):
    models = models
    sentences = readData("sentiment_analysis/corpus.txt")
    tokenizedWords = tokenizeWords(sentences)
    
    # Generate Word2Vec Model
    for model in models:
        w2v_model = movieFeedbackWord2Vec(tokenizedWords, model_type=model)
        w2v_model.save(f'vec_models/{model}_model.bin')
    
    print("Succesfully")

if __name__ == "__main__":
    createW2VModel(models = ["skipgram"])