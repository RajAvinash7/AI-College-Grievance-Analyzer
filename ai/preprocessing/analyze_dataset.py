import pandas as pd


TRAIN_PATH = "dataset/raw/train.csv"
TEST_PATH = "dataset/raw/test.csv"


# ============================================================
# LOAD DATA
# ============================================================

train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

df = pd.concat(
    [train_df.assign(split="train"),
     test_df.assign(split="test")],
    ignore_index=True
)


# ============================================================
# BASIC INFORMATION
# ============================================================

print("=" * 70)
print("DATASET ANALYSIS")
print("=" * 70)

print("\nTotal complaints:", len(df))
print("Training complaints:", len(train_df))
print("Testing complaints:", len(test_df))


# ============================================================
# CATEGORIES
# ============================================================

print("\n" + "=" * 70)
print("CATEGORIES")
print("=" * 70)

print(df["Category"].value_counts())


# ============================================================
# SEVERITY
# ============================================================

print("\n" + "=" * 70)
print("SEVERITY")
print("=" * 70)

print(df["Severity"].value_counts())


# ============================================================
# PRIMARY DEPARTMENTS
# ============================================================

print("\n" + "=" * 70)
print("PRIMARY DEPARTMENTS")
print("=" * 70)

print(df["Primary_Department"].value_counts())


# ============================================================
# RESPONSIBLE DEPARTMENTS
# ============================================================

print("\n" + "=" * 70)
print("RESPONSIBLE DEPARTMENTS")
print("=" * 70)

print(
    df["Responsible_Departments"]
    .value_counts()
    .head(20)
)


# ============================================================
# ASPECTS
# ============================================================

print("\n" + "=" * 70)
print("ASPECTS")
print("=" * 70)

print(
    df["Aspects"]
    .value_counts()
    .head(30)
)


# ============================================================
# COMPLAINT GROUPS
# ============================================================

print("\n" + "=" * 70)
print("COMPLAINT GROUPS")
print("=" * 70)

group_counts = df["Complaint_Group_ID"].value_counts()

print("Unique complaint groups:", group_counts.nunique())
print("Total unique group IDs:", df["Complaint_Group_ID"].nunique())

print("\nLargest complaint groups:")
print(group_counts.head(20))


# ============================================================
# CHECK GROUP LEAKAGE
# ============================================================

print("\n" + "=" * 70)
print("TRAIN / TEST GROUP OVERLAP")
print("=" * 70)

train_groups = set(train_df["Complaint_Group_ID"])
test_groups = set(test_df["Complaint_Group_ID"])

overlap = train_groups.intersection(test_groups)

print("Groups in training:", len(train_groups))
print("Groups in testing:", len(test_groups))
print("Groups appearing in BOTH:", len(overlap))

if overlap:
    print("\nPotential leakage groups:")
    print(sorted(overlap))
else:
    print("\nNo complaint groups overlap between train and test.")


# ============================================================
# DUPLICATE COMPLAINTS
# ============================================================

print("\n" + "=" * 70)
print("DUPLICATE COMPLAINTS")
print("=" * 70)

duplicates = df[
    df["Complaint_Description"].duplicated(keep=False)
].sort_values("Complaint_Description")

print("Duplicate complaint rows:", len(duplicates))

if len(duplicates) > 0:
    print("\nExamples:")
    print(
        duplicates[
            ["Complaint_Description", "Category", "Severity"]
        ].head(20).to_string(index=False)
    )


# ============================================================
# SAMPLE COMPLAINTS BY CATEGORY
# ============================================================

print("\n" + "=" * 70)
print("SAMPLE COMPLAINTS BY CATEGORY")
print("=" * 70)

for category in sorted(df["Category"].unique()):

    print("\n" + "-" * 60)
    print(category)
    print("-" * 60)

    samples = df[df["Category"] == category].head(5)

    for _, row in samples.iterrows():

        print(
            f"\nComplaint: {row['Complaint_Description']}"
        )

        print(
            f"Severity: {row['Severity']}"
        )

        print(
            f"Department: {row['Primary_Department']}"
        )

        print(
            f"Aspect: {row['Aspects']}"
        )