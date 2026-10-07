import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_PATH = BASE_DIR / "dataset" / "raw" / "train.csv"
TEST_PATH = BASE_DIR / "dataset" / "raw" / "test.csv"

OUTPUT_DIR = BASE_DIR / "dataset" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD RAW DATA
# ============================================================

train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)


print("=" * 60)
print("PREPARING DATASET")
print("=" * 60)

print("Training rows:", len(train_df))
print("Testing rows:", len(test_df))


# ============================================================
# SELECT RELEVANT COLUMNS
# ============================================================

columns = [
    "Complaint_Description",
    "Category",
    "Severity",
    "Primary_Department"
]

train_processed = train_df[columns].copy()
test_processed = test_df[columns].copy()


# ============================================================
# RENAME COLUMNS
# ============================================================

train_processed.rename(
    columns={
        "Complaint_Description": "text",
        "Category": "category",
        "Severity": "severity",
        "Primary_Department": "department"
    },
    inplace=True
)

test_processed.rename(
    columns={
        "Complaint_Description": "text",
        "Category": "category",
        "Severity": "severity",
        "Primary_Department": "department"
    },
    inplace=True
)


# ============================================================
# CLEAN TEXT
# ============================================================

for df in [train_processed, test_processed]:

    df["text"] = (
        df["text"]
        .astype(str)
        .str.strip()
    )


# ============================================================
# REMOVE EMPTY TEXT
# ============================================================

train_processed = train_processed[
    train_processed["text"].str.len() > 0
]

test_processed = test_processed[
    test_processed["text"].str.len() > 0
]


# ============================================================
# SAVE PROCESSED DATA
# ============================================================

train_output = OUTPUT_DIR / "train_processed.csv"
test_output = OUTPUT_DIR / "test_processed.csv"

train_processed.to_csv(
    train_output,
    index=False
)

test_processed.to_csv(
    test_output,
    index=False
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\nProcessed training rows:", len(train_processed))
print("Processed testing rows:", len(test_processed))

print("\nColumns:")
print(train_processed.columns.tolist())

print("\nCategory distribution:")
print(train_processed["category"].value_counts())

print("\nSeverity distribution:")
print(train_processed["severity"].value_counts())

print("\nDepartment distribution:")
print(train_processed["department"].value_counts())

print("\nSaved:")
print(train_output)
print(test_output)

print("\nDataset preparation completed!")