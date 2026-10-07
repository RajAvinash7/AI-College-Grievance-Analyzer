import pandas as pd
import joblib
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_PATH = BASE_DIR / "dataset" / "processed" / "train_processed.csv"
TEST_PATH = BASE_DIR / "dataset" / "processed" / "test_processed.csv"

MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)


# ============================================================
# CREATE CONTEXT-AWARE TEXT
# ============================================================

def create_context_text(df):

    return (
        "Category: "
        + df["category"].astype(str)
        + " | Complaint: "
        + df["text"].astype(str)
    )


X_train = create_context_text(train_df)
y_train = train_df["severity"]

X_test = create_context_text(test_df)
y_test = test_df["severity"]


print("=" * 70)
print("TF-IDF + LOGISTIC REGRESSION")
print("CONTEXT-AWARE SEVERITY CLASSIFIER")
print("=" * 70)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

print("\nSeverity distribution:")
print(y_train.value_counts())


# ============================================================
# SHOW EXAMPLE
# ============================================================

print("\nExample input:")
print(X_train.iloc[0])


# ============================================================
# TF-IDF
# ============================================================

print("\nCreating TF-IDF features...")

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2),
    sublinear_tf=True
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("Training feature shape:")
print(X_train_tfidf.shape)


# ============================================================
# TRAIN
# ============================================================

print("\nTraining Logistic Regression...")

classifier = LogisticRegression(
    max_iter=2000,
    class_weight="balanced"
)

classifier.fit(
    X_train_tfidf,
    y_train
)

print("Training completed!")


# ============================================================
# PREDICTION
# ============================================================

y_pred = classifier.predict(X_test_tfidf)


# ============================================================
# EVALUATION
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n" + "=" * 70)
print("RESULTS")
print("=" * 70)

print(f"\nAccuracy: {accuracy:.4f}")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

labels = sorted(y_test.unique())

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

print("\nConfusion Matrix:")
print("Labels:")
print(labels)
print(cm)


# ============================================================
# SAVE
# ============================================================

MODEL_PATH = MODEL_DIR / "severity_context_classifier.joblib"
VECTORIZER_PATH = MODEL_DIR / "severity_context_vectorizer.joblib"

joblib.dump(
    classifier,
    MODEL_PATH
)

joblib.dump(
    vectorizer,
    VECTORIZER_PATH
)

print("\nClassifier saved to:")
print(MODEL_PATH)

print("\nVectorizer saved to:")
print(VECTORIZER_PATH)

print("\nExperiment completed!")