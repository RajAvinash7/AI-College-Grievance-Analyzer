import numpy as np


def calculate_similarity(embedding1, embedding2):
    """
    Calculate cosine similarity between two normalized embeddings.
    """

    similarity = np.dot(embedding1, embedding2)

    return float(similarity)


def find_similar_grievances(
    new_embedding,
    grievances,
    threshold=0.60,
    top_k=3
):
    """
    Find the most similar previous grievances.

    Parameters:
        new_embedding: embedding of the new complaint
        grievances: list of previous grievances with embeddings
        threshold: minimum similarity required
        top_k: maximum number of results

    Returns:
        List of similar grievances sorted by similarity.
    """

    results = []

    for grievance in grievances:

        similarity = calculate_similarity(
            new_embedding,
            grievance["embedding"]
        )

        if similarity >= threshold:

            results.append({
                "id": grievance["id"],
                "complaint": grievance["complaint"],
                "similarity": similarity
            })

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results[:top_k]