import pandas as pd


TRAIN_PATH = "dataset/raw/train.csv"
TEST_PATH = "dataset/raw/test.csv"


train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)


# Normalize text for comparison
train_text = (
    train_df["Complaint_Description"]
    .astype(str)
    .str.lower()
    .str.strip()
)

test_text = (
    test_df["Complaint_Description"]
    .astype(str)
    .str.lower()
    .str.strip()
)


overlap = set(train_text).intersection(set(test_text))


print("=" * 60)
print("TRAIN / TEST DUPLICATE CHECK")
print("=" * 60)

print("Unique complaints in train:", train_text.nunique())
print("Unique complaints in test:", test_text.nunique())

print("Exact complaints appearing in BOTH:", len(overlap))


if overlap:

    print("\nOverlapping complaints:\n")

    for complaint in sorted(overlap):
        print("-", complaint)

else:

    print("\nNo exact complaint text appears in both train and test.")