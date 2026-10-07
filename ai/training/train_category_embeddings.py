import pandas as pd
import joblib

from pathlib import Path

from sentence_transformers import SentenceTransformer

from sklearn.svm import LinearSVC
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

X_train = train_df["text"].tolist()
y_train = train_df["category"]

X_test = test_df["text"].tolist()
y_test = test_df["category"]


print("=" * 70)
print("SENTENCE TRANSFORMER + LINEAR SVM")
print("=" * 70)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("\nLoading embedding model:")
print(MODEL_NAME)

encoder = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded!")


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

print("\nCreating training embeddings...")

X_train_embeddings = encoder.encode(
    X_train,
    show_progress_bar=True
)

print("\nCreating testing embeddings...")

X_test_embeddings = encoder.encode(
    X_test,
    show_progress_bar=True
)


print("\nEmbedding shape:")
print(X_train_embeddings.shape)


# ============================================================
# TRAIN CLASSIFIER
# ============================================================

print("\nTraining Linear SVM...")

classifier = LinearSVC(
    class_weight="balanced"
)

classifier.fit(
    X_train_embeddings,
    y_train
)

print("Training completed!")


# ============================================================
# PREDICTION
# ============================================================

y_pred = classifier.predict(X_test_embeddings)


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
# SAVE CLASSIFIER
# ============================================================

CLASSIFIER_PATH = (
    MODEL_DIR /
    "category_embedding_classifier.joblib"
)

joblib.dump(
    classifier,
    CLASSIFIER_PATH
)

print("\nClassifier saved to:")
print(CLASSIFIER_PATH)


# ============================================================
# SAVE EMBEDDING MODEL NAME
# ============================================================

print("\nEmbedding model used:")
print(MODEL_NAME)

print("\nExperiment completed!")