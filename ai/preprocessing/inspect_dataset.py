import pandas as pd

TRAIN_PATH = "dataset/raw/train.csv"
TEST_PATH = "dataset/raw/test.csv"

# Load datasets
train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)


print("=" * 60)
print("TRAIN DATASET")
print("=" * 60)

print("Shape:", train_df.shape)

print("\nColumns:")
print(train_df.columns.tolist())


print("\nFirst 5 rows:")
print(train_df.head())


print("\nMissing values:")
print(train_df.isnull().sum())


print("\nCategory distribution:")
print(train_df["Category"].value_counts())


print("\nSeverity distribution:")
print(train_df["Severity"].value_counts())


print("\nPrimary department distribution:")
print(train_df["Primary_Department"].value_counts())


print("\nUnique complaint groups:")
print(train_df["Complaint_Group_ID"].nunique())


print("\n" + "=" * 60)
print("TEST DATASET")
print("=" * 60)

print("Shape:", test_df.shape)

print("\nCategory distribution:")
print(test_df["Category"].value_counts())


print("\nSeverity distribution:")
print(test_df["Severity"].value_counts())


print("\nFirst 5 complaints:")
for i, row in test_df.head().iterrows():
    print("\nComplaint:", row["Complaint_Description"])
    print("Category:", row["Category"])
    print("Severity:", row["Severity"])