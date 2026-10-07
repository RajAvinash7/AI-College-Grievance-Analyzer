import pandas as pd
import joblib

from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_PATH = (
    BASE_DIR
    / "dataset"
    / "processed"
    / "train_processed.csv"
)

TEST_PATH = (
    BASE_DIR
    / "dataset"
    / "processed"
    / "test_processed.csv"
)

MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)


X_train = train_df["text"]
y_train = train_df["category"]

X_test = test_df["text"]
y_test = test_df["category"]


print("=" * 70)
print("CATEGORY CLASSIFIER")
print("=" * 70)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

print("\nCategories:")
print(y_train.value_counts())


# ============================================================
# BUILD PIPELINE
# ============================================================

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True
        )
    ),

    (
        "classifier",
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced"
        )
    )
])


# ============================================================
# TRAIN
# ============================================================

print("\nTraining model...")

model.fit(X_train, y_train)

print("Training completed!")


# ============================================================
# PREDICTION
# ============================================================

y_pred = model.predict(X_test)


# ============================================================
# EVALUATION
# ============================================================

accuracy = accuracy_score(y_test, y_pred)

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
# SAVE MODEL
# ============================================================

MODEL_PATH = MODEL_DIR / "category_classifier.joblib"

joblib.dump(model, MODEL_PATH)

print("\nModel saved to:")
print(MODEL_PATH)


# ============================================================
# TEST SOME NEW GRIEVANCES
# ============================================================

test_complaints = [
    "The WiFi is not working in the computer laboratory.",
    "The classroom projector is broken.",
    "My examination marks are incorrect.",
    "The university fee payment system is not working.",
    "There are not enough qualified teachers in our department."
]


print("\n" + "=" * 70)
print("SAMPLE PREDICTIONS")
print("=" * 70)

predictions = model.predict(test_complaints)
probabilities = model.predict_proba(test_complaints)

for complaint, prediction, probability in zip(
    test_complaints,
    predictions,
    probabilities
):

    confidence = probability.max()

    print("\nComplaint:")
    print(complaint)

    print("Predicted category:", prediction)
    print(f"Confidence: {confidence:.2%}")