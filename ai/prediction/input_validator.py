from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re


# ============================================================
# LOAD SEMANTIC MODEL
# ============================================================

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading input validation model...")

encoder = SentenceTransformer(MODEL_NAME)

print("Validation model loaded!")


# ============================================================
# REFERENCE SENTENCES
# ============================================================
#
# These are examples of what a genuine college grievance
# generally looks like.
#
# The model compares the user's complaint semantically
# against these examples.
# ============================================================

REFERENCE_COMPLAINTS = [
    "The WiFi in my college is not working.",
    "The internet connection in the college is very slow.",
    "The examination portal is not showing my marks.",
    "I have a problem with my examination results.",
    "My college fees were charged incorrectly.",
    "I have not received my scholarship.",
    "The classroom equipment is not working.",
    "There is no water supply in the hostel.",
    "The hostel room needs maintenance.",
    "The college library has a problem.",
    "I cannot register for my course.",
    "The teacher is not available for our class.",
    "I have an issue with my student ID card.",
    "The college transport service is not working properly.",
    "The college website is not working.",
    "There is an electrical problem in the classroom."
]


# Create embeddings once
REFERENCE_EMBEDDINGS = encoder.encode(
    REFERENCE_COMPLAINTS
)


# ============================================================
# HELPER: GIBBERISH CHECK
# ============================================================

def looks_like_gibberish(text):

    normalized = re.sub(
        r"[^a-zA-Z\s]",
        "",
        text.lower()
    )

    normalized = " ".join(normalized.split())

    words = normalized.split()

    if not words:
        return True


    # Extremely long words without vowels are suspicious
    suspicious_words = 0

    for word in words:

        if len(word) >= 6:

            if not re.search(r"[aeiou]", word):
                suspicious_words += 1


    if suspicious_words >= 1:
        return True


    return False


# ============================================================
# MAIN VALIDATION FUNCTION
# ============================================================

def validate_complaint(text):

    # --------------------------------------------------------
    # 1. Basic input check
    # --------------------------------------------------------

    if text is None:
        return False, "Please enter a complaint.", 0.0

    text = text.strip()

    if not text:
        return False, "Please enter a complaint.", 0.0


    # --------------------------------------------------------
    # 2. Minimum length
    # --------------------------------------------------------

    if len(text) < 5:
        return (
            False,
            "Complaint is too short. Please describe your issue.",
            0.0
        )


    # --------------------------------------------------------
    # 3. Gibberish detection
    # --------------------------------------------------------

    if looks_like_gibberish(text):

        return (
            False,
            "The input does not appear to be meaningful text.",
            0.0
        )


    # --------------------------------------------------------
    # 4. Semantic similarity
    # --------------------------------------------------------

    input_embedding = encoder.encode([text])

    similarities = cosine_similarity(
        input_embedding,
        REFERENCE_EMBEDDINGS
    )[0]

    max_similarity = float(similarities.max())


    # --------------------------------------------------------
    # 5. Validation threshold
    # --------------------------------------------------------
    #
    # If the complaint is sufficiently similar to examples
    # of genuine college grievances, accept it.
    #
    # Otherwise reject it.
    # --------------------------------------------------------

    THRESHOLD = 0.35

    if max_similarity < THRESHOLD:

        return (
            False,
            "This does not appear to be a college-related grievance.",
            max_similarity
        )


    # --------------------------------------------------------
    # Valid complaint
    # --------------------------------------------------------

    return (
        True,
        "Valid college grievance.",
        max_similarity
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_inputs = [

        # Garbage
        "ok",
        "hello",
        "blah blah",
        "asdfghjkl",

        # Valid short complaint
        "WiFi is down",

        # Valid complaints
        "The WiFi in our college library is not working.",
        "The examination portal is not showing my marks.",
        "My hostel room has a water problem.",

        # Unrelated
        "What is the capital of France?",
        "I want to buy a new phone."
    ]


    print("\n" + "=" * 70)
    print("INPUT VALIDATOR TEST")
    print("=" * 70)


    for text in test_inputs:

        valid, message, similarity = validate_complaint(text)

        print("\nInput:")
        print(text)

        print("Valid:")
        print(valid)

        print("Similarity:")
        print(f"{similarity:.4f}")

        print("Message:")
        print(message)