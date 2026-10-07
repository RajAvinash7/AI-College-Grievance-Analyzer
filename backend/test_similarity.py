from backend.grievance_repository import find_similar_grievances
from ai.prediction.embedding_model import encoder


# ============================================================
# NEW COMPLAINT
# ============================================================

complaint = (
    "The hostel drinking water supply has stopped "
    "and students cannot get water."
)


# ============================================================
# CREATE EMBEDDING
# ============================================================

embedding = encoder.encode(
    [complaint],
    normalize_embeddings=True
)


# ============================================================
# FIND SIMILAR GRIEVANCES
# ============================================================

results = find_similar_grievances(
    new_embedding=embedding,
    threshold=0.60,
    top_k=3
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 70)
print("NEW COMPLAINT")
print("=" * 70)

print("\n", complaint)

print("\n" + "=" * 70)
print("SIMILAR GRIEVANCES")
print("=" * 70)


if not results:

    print("\nNo similar grievances found.")

else:

    for index, grievance in enumerate(
        results,
        start=1
    ):

        print(
            f"\n#{index} "
            f"Grievance ID: {grievance['id']}"
        )

        print(
            "Similarity:",
            f"{grievance['similarity']:.4f}"
        )

        print(
            "Category:",
            grievance["category"]
        )

        print(
            "Severity:",
            grievance["severity"]
        )

        print(
            "Department:",
            grievance["department"]
        )

        print(
            "Complaint:",
            grievance["complaint"]
        )


print("\n" + "=" * 70)