import joblib
from pathlib import Path

from ai.prediction.embedding_model import encoder
from ai.prediction.input_validator import validate_complaint


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"


# ============================================================
# MODEL PATHS
# ============================================================

CATEGORY_MODEL_PATH = (
    MODEL_DIR / "category_embedding_classifier.joblib"
)

DEPARTMENT_MODEL_PATH = (
    MODEL_DIR / "department_embedding_classifier.joblib"
)

SEVERITY_MODEL_PATH = (
    MODEL_DIR / "severity_context_classifier.joblib"
)

SEVERITY_VECTORIZER_PATH = (
    MODEL_DIR / "severity_context_vectorizer.joblib"
)


# ============================================================
# LOAD MODELS
# ============================================================

print("Loading shared MiniLM embedding model...")


print("Loading category classifier...")

category_model = joblib.load(
    CATEGORY_MODEL_PATH
)


print("Loading department classifier...")

department_model = joblib.load(
    DEPARTMENT_MODEL_PATH
)


print("Loading severity classifier...")

severity_model = joblib.load(
    SEVERITY_MODEL_PATH
)


print("Loading severity TF-IDF vectorizer...")

severity_vectorizer = joblib.load(
    SEVERITY_VECTORIZER_PATH
)


print("All models loaded successfully!")


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_grievance(text):

    # --------------------------------------------------------
    # STEP 1: Validate complaint
    # --------------------------------------------------------

    valid, message, similarity = validate_complaint(text)

    if not valid:

        return {
            "valid": False,
            "message": message,
            "similarity": similarity,
            "complaint": text
        }


    # --------------------------------------------------------
    # STEP 2: Create MiniLM embedding
    # --------------------------------------------------------

    embedding = encoder.encode(
        [text],
        normalize_embeddings=True
    )


    # --------------------------------------------------------
    # STEP 3: Predict Category
    # --------------------------------------------------------

    category = category_model.predict(
        embedding
    )[0]


    # --------------------------------------------------------
    # STEP 4: Predict Department
    # --------------------------------------------------------

    department = department_model.predict(
        embedding
    )[0]


    # --------------------------------------------------------
    # STEP 5: Prepare input for Severity model
    #
    # Severity model was trained using:
    #
    # Category + Complaint
    # --------------------------------------------------------

    severity_input = (
        "Category: "
        + str(category)
        + " | Complaint: "
        + str(text)
    )


    # --------------------------------------------------------
    # STEP 6: Convert severity input to TF-IDF
    # --------------------------------------------------------

    severity_features = severity_vectorizer.transform(
        [severity_input]
    )


    # --------------------------------------------------------
    # STEP 7: Predict Severity
    # --------------------------------------------------------

    severity = severity_model.predict(
        severity_features
    )[0]


    # --------------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------------

    return {
        "valid": True,
        "message": message,
        "similarity": similarity,
        "complaint": text,
        "category": category,
        "severity": severity,
        "department": department,
        "embedding": embedding
    }


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("AI COLLEGE GRIEVANCE ANALYZER")
    print("=" * 70)


    complaint = input(
        "\nEnter student complaint: "
    )


    result = predict_grievance(
        complaint
    )


    # ========================================================
    # INVALID COMPLAINT
    # ========================================================

    if not result["valid"]:

        print("\n" + "=" * 70)
        print("COMPLAINT REJECTED")
        print("=" * 70)

        print("\nComplaint:")
        print(result["complaint"])

        print("\nReason:")
        print(result["message"])

        print(
            "\nSimilarity score:",
            f"{result['similarity']:.4f}"
        )

        print(
            "\nPlease enter a meaningful "
            "college-related grievance."
        )

        print("\n" + "=" * 70)


    # ========================================================
    # VALID COMPLAINT
    # ========================================================

    else:

        print("\n" + "=" * 70)
        print("PREDICTION")
        print("=" * 70)

        print("\nComplaint:")
        print(result["complaint"])

        print("\nValidation:")
        print("Valid college grievance")

        print(
            "Similarity score:",
            f"{result['similarity']:.4f}"
        )

        print("\nCategory:")
        print(result["category"])

        print("\nSeverity:")
        print(result["severity"])

        print("\nResponsible Department:")
        print(result["department"])

        print("\nEmbedding:")
        print(
            f"Generated {len(result['embedding'][0])}-dimensional embedding"
        )

        print("\n" + "=" * 70)