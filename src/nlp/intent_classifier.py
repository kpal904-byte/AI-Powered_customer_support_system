import pickle

from src.config.settings import settings
from src.data.preprocessing import clean_text


class IntentClassifier:
    """
    Loads the trained TF-IDF + Logistic Regression
    model and predicts customer intent.
    """

    def __init__(self):

        model_path = (
            settings.MODEL_DIR /
            "intent_classifier.pkl"
        )

        vectorizer_path = (
            settings.MODEL_DIR /
            "tfidf_vectorizer.pkl"
        )

        if not model_path.exists():
            raise FileNotFoundError(
                f"Intent model not found: {model_path}"
            )

        if not vectorizer_path.exists():
            raise FileNotFoundError(
                f"TF-IDF vectorizer not found: {vectorizer_path}"
            )

        with open(model_path, "rb") as file:
            self.model = pickle.load(file)

        with open(vectorizer_path, "rb") as file:
            self.vectorizer = pickle.load(file)

    def predict(self, text: str) -> dict:
        """
        Predict intent and confidence.
        """

        cleaned_text = clean_text(text)

        vector = self.vectorizer.transform(
            [cleaned_text]
        )

        intent = self.model.predict(vector)[0]

        probabilities = self.model.predict_proba(vector)[0]

        confidence = float(probabilities.max())

        return {
            "intent": intent,
            "confidence": confidence,
        }


if __name__ == "__main__":

    classifier = IntentClassifier()

    test_queries = [
        "I want to return my product",
        "Where is my order?",
        "My payment failed",
        "I forgot my password",
        "My laptop is overheating",
    ]

    for query in test_queries:

        result = classifier.predict(query)

        print("\nQuery:", query)
        print("Intent:", result["intent"])
        print(
            "Confidence:",
            round(result["confidence"], 3)
        )