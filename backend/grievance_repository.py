from backend.database import get_connection


# ============================================================
# SAVE GRIEVANCE
# ============================================================

def save_grievance(
    complaint,
    category,
    severity,
    department,
    similarity,
    embedding
):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        query = """
            INSERT INTO grievance
            (
                complaint,
                category,
                severity,
                department,
                similarity,
                embedding
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """

        cursor.execute(
            query,
            (
                complaint,
                category,
                severity,
                department,
                similarity,
                embedding.tolist()[0]
                if hasattr(embedding, "tolist")
                else embedding
            )
        )

        grievance_id = cursor.fetchone()[0]

        conn.commit()

        return grievance_id

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


# ============================================================
# GET ALL GRIEVANCES
# ============================================================

def get_all_grievances():

    conn = get_connection()

    try:
        cursor = conn.cursor()

        query = """
            SELECT
                id,
                complaint,
                category,
                severity,
                department,
                similarity,
                created_at
            FROM grievance
            ORDER BY created_at DESC;
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        grievances = []

        for row in rows:

            grievances.append({
                "id": row[0],
                "complaint": row[1],
                "category": row[2],
                "severity": row[3],
                "department": row[4],
                "similarity": row[5],
                "created_at": (
                    row[6].isoformat()
                    if row[6]
                    else None
                )
            })

        return grievances

    finally:
        cursor.close()
        conn.close()


# ============================================================
# FIND SIMILAR GRIEVANCES
# ============================================================

def find_similar_grievances(
    new_embedding,
    exclude_id=None,
    threshold=0.60,
    top_k=3
):
    """
    Find previous grievances that are semantically
    similar to the new complaint.

    Parameters:
        new_embedding:
            384-dimensional MiniLM embedding.

        exclude_id:
            Grievance ID to exclude from the search.

        threshold:
            Minimum similarity required.

        top_k:
            Maximum number of results.

    Returns:
        List of similar grievances.
    """

    conn = get_connection()

    try:
        cursor = conn.cursor()

        query = """
            SELECT
                id,
                complaint,
                category,
                severity,
                department,
                embedding
            FROM grievance
            WHERE embedding IS NOT NULL
        """

        params = []

        if exclude_id is not None:

            query += """
                AND id != %s
            """

            params.append(exclude_id)

        cursor.execute(
            query,
            tuple(params)
        )

        rows = cursor.fetchall()

        results = []

        # ----------------------------------------------------
        # Convert new embedding into a flat list
        # ----------------------------------------------------

        if hasattr(new_embedding, "tolist"):

            new_embedding = new_embedding.tolist()

        if len(new_embedding) == 1:

            new_embedding = new_embedding[0]

        # ----------------------------------------------------
        # Compare against every stored embedding
        # ----------------------------------------------------

        for row in rows:

            grievance_id = row[0]
            complaint = row[1]
            category = row[2]
            severity = row[3]
            department = row[4]
            stored_embedding = row[5]

            if not stored_embedding:
                continue

            # ------------------------------------------------
            # Cosine similarity
            # ------------------------------------------------

            dot_product = sum(
                a * b
                for a, b in zip(
                    new_embedding,
                    stored_embedding
                )
            )

            new_norm = sum(
                a * a
                for a in new_embedding
            ) ** 0.5

            stored_norm = sum(
                a * a
                for a in stored_embedding
            ) ** 0.5

            if new_norm == 0 or stored_norm == 0:
                continue

            similarity_score = (
                dot_product
                / (new_norm * stored_norm)
            )

            # ------------------------------------------------
            # Apply threshold
            # ------------------------------------------------

            if similarity_score >= threshold:

                results.append({
                    "id": grievance_id,
                    "complaint": complaint,
                    "category": category,
                    "severity": severity,
                    "department": department,
                    "similarity": float(
                        similarity_score
                    )
                })

        # ----------------------------------------------------
        # Highest similarity first
        # ----------------------------------------------------

        results.sort(
            key=lambda x: x["similarity"],
            reverse=True
        )

        return results[:top_k]

    finally:
        cursor.close()
        conn.close()