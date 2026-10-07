from backend.database import get_connection
from ai.prediction.embedding_model import encoder


# ============================================================
# BACKFILL MISSING GRIEVANCE EMBEDDINGS
# ============================================================

conn = get_connection()

try:

    cursor = conn.cursor()

    # --------------------------------------------------------
    # Get grievances that don't have embeddings
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT id, complaint
        FROM grievance
        WHERE embedding IS NULL
        ORDER BY id;
        """
    )

    rows = cursor.fetchall()

    print("\n" + "=" * 70)
    print("GRIEVANCE EMBEDDING BACKFILL")
    print("=" * 70)

    print(
        f"\nFound {len(rows)} grievances without embeddings."
    )


    # --------------------------------------------------------
    # Process each grievance
    # --------------------------------------------------------

    for grievance_id, complaint in rows:

        print(
            f"\nProcessing grievance #{grievance_id}..."
        )

        # Generate 384-dimensional embedding
        embedding = encoder.encode(
            [complaint],
            normalize_embeddings=True
        )

        # Convert (1, 384) NumPy array
        # into a flat Python list of 384 values
        embedding_list = embedding.tolist()[0]

        # Save embedding
        cursor.execute(
            """
            UPDATE grievance
            SET embedding = %s
            WHERE id = %s;
            """,
            (
                embedding_list,
                grievance_id
            )
        )

        print(
            f"✓ Grievance #{grievance_id} updated "
            f"({len(embedding_list)} dimensions)"
        )


    # --------------------------------------------------------
    # Commit changes
    # --------------------------------------------------------

    conn.commit()

    print("\n" + "=" * 70)
    print("BACKFILL COMPLETE")
    print("=" * 70)

    print(
        f"\nUpdated {len(rows)} grievances."
    )


except Exception as error:

    conn.rollback()

    print("\n❌ Backfill failed:")
    print(error)

    raise


finally:

    cursor.close()
    conn.close()