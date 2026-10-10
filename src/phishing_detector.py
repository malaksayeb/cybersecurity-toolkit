import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline


class PhishingDetector:

  def __init__(self):
    self.model = None

  def train_dummy_model(self):
    """Entraîne un modèle d'exemple rapide pour le prototype."""
    X = [
        (
            "Dear user, click here to reset your bank password immediately or"
            " your account will be suspended."
        ),
        "Hey team, let's schedule the meeting for tomorrow morning at 10 AM.",
        "URGENT: Verify your crypto wallet security now to avoid permanent loss.",
        "Here is the weekly report for the engineering department project status.",
        "You have won a free iPhone click this link to claim your prize.",
    ]
    y = [1, 0, 1, 0, 1]  # 1 = Phishing, 0 = Safe

    self.model = Pipeline([
        ("tfidf", TfidfVectorizer(stop_words="english")),
        (
            "clf",
            RandomForestClassifier(n_estimators=50, random_state=42),
        ),
    ])
    self.model.fit(X, y)

  def predict_email(self, text: str) -> dict:
    if not self.model:
      self.train_dummy_model()

    prediction = self.model.predict([text])[0]
    probability = max(self.model.predict_proba([text])[0])

    urls = re.findall(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        text,
    )

    return {
        "is_phishing": bool(prediction),
        "confidence": round(float(probability) * 100, 2),
        "extracted_urls": urls,
    }