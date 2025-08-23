import pickle

def load_model():
    # loads pretrained model
    with open("models/sentiment_model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    with open("models/tfidf_vectorizer.pkl", "rb") as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    return model, vectorizer