import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from sklearn.metrics import classification_report, confusion_matrix

import joblib


# ==========================================
# 1. LOAD DATASET
# ==========================================

DATA_PATH = "../dataset/grievances.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded!")
print("Number of grievances:", len(df))

print("\nCategories:")
print(df["category"].value_counts())


# ==========================================
# 2. INPUT AND TARGET
# ==========================================

X = df["text"]
y = df["category"]


# ==========================================
# 3. TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 4. BUILD MODEL
# ==========================================

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])


# ==========================================
# 5. TRAIN
# ==========================================

print("\nTraining model...")

model.fit(X_train, y_train)

print("Training completed!")


# ==========================================
# 6. PREDICTION
# ==========================================

y_pred = model.predict(X_test)


# ==========================================
# 7. EVALUATION
# ==========================================

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# ==========================================
# 8. SAVE MODEL
# ==========================================

MODEL_PATH = "../models/grievance_classifier.joblib"

joblib.dump(model, MODEL_PATH)

print("\nModel saved to:")
print(MODEL_PATH)