# %% [markdown]
# # E-commerce customer churn: first look
# Run this file from top to bottom. Sections marked YOUR TURN are exercises.
# This stage checks the source data; it does not fit models or clean values.
# Read README.md alongside the code and record your reasoning in NOTES.md.

# %%
# 1. Import the tools and locate the workbook.
# pathlib is built into Python. pandas supplies DataFrames (tables in memory).
# openpyxl is installed as pandas' Excel-reading engine; no direct import needed.
from pathlib import Path
import pandas as pd

# A .py file knows its own location through __file__. A notebook uses its
# working directory instead: open the notebook from this project folder.
PROJECT_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
DATA_PATH = PROJECT_DIR / "data" / "raw" / "E Commerce Dataset.xlsx"
if not DATA_PATH.is_file():
    raise FileNotFoundError(
        f"Workbook not found at {DATA_PATH}. Open/run from the project folder; "
        "keep the supplied data/raw folder with the code."
    )

print("pandas version:", pd.__version__)
print("Reading:", DATA_PATH)

# %% [markdown]
# ## 2. Load the right sheets
# The first sheet is a dictionary, not the customer table. Naming the sheet
# prevents accidentally analyzing the dictionary. The context manager closes
# the workbook after loading. raw_df stays untouched; df is your working copy.

# %%
with pd.ExcelFile(DATA_PATH, engine="openpyxl") as workbook:
    print("Available sheets:", workbook.sheet_names)
    raw_df = pd.read_excel(workbook, sheet_name="E Comm")
    # The dictionary's headings are on Excel row 2, so header=1 is zero-based.
    source_dictionary = pd.read_excel(workbook, sheet_name="Data Dict", header=1)

df = raw_df.copy(deep=True)
print(f"Rows: {df.shape[0]:,}; columns: {df.shape[1]}")
print("Column names:", df.columns.tolist())
print(df.head().to_string(index=False))
print("\nWorkbook dictionary (original descriptions):")
print(source_dictionary.dropna(axis=1, how="all").to_string(index=False))

# %% [markdown]
# ## 3. Understand structure before choosing features
# info() prints storage types and nonmissing counts. A numeric storage type
# does not imply a numeric measurement: CustomerID is an identifier, CityTier
# is a code, and Churn is an outcome. None should enter k-means as a measurement.
# Preserve the workbook's spellings (including PreferedOrderCat) for now.

# %%
df.info()

# These lists describe how we inspect columns, not a final model feature list.
category_columns = [
    "PreferredLoginDevice", "PreferredPaymentMode", "Gender",
    "PreferedOrderCat", "MaritalStatus",
]
measurement_columns = [
    "Tenure", "WarehouseToHome", "HourSpendOnApp", "NumberOfDeviceRegistered",
    "NumberOfAddress", "OrderAmountHikeFromlastYear", "CouponUsed",
    "OrderCount", "DaySinceLastOrder", "CashbackAmount",
]

# %% [markdown]
# ## 4. Build a column audit
# isna() marks missing cells True. Summing True values counts missing cells;
# their mean is the missing fraction. Multiplying by 100 makes a percentage.
# nunique(dropna=True) counts distinct observed values, excluding missing ones.
# Sorting changes this summary table, not the customer rows.

# %%
column_audit = pd.DataFrame({
    "dtype": df.dtypes.astype(str),
    "missing_count": df.isna().sum(),
    "missing_pct": df.isna().mean().mul(100).round(2),
    "distinct_nonmissing": df.nunique(dropna=True),
}).sort_values("missing_count", ascending=False)
print(column_audit.to_string())

# axis=1 means inspect across columns within each row. Column-level missing
# percentages cannot simply be added to infer the number of affected rows.
incomplete_rows = df.isna().any(axis=1)
print(f"\nRows with at least one missing value: {incomplete_rows.sum():,}")
print(f"Share of rows affected: {incomplete_rows.mean():.2%}")
print("Rows left if all incomplete rows were dropped:", (~incomplete_rows).sum())

# YOUR TURN: Explain in NOTES.md why missing does not mean zero. Decide what
# more you need to know before choosing an eventual missing-value strategy.

# %% [markdown]
# ## 5. Check identity and repeated records
# duplicated() counts repeats after the first occurrence, not all members of
# duplicate groups. Different IDs can still share the same measured profile.
# A repeated profile is a question to investigate, not proof of bad data.

# %%
print("Missing IDs:", df["CustomerID"].isna().sum())
print("Repeated IDs after first:", df["CustomerID"].duplicated().sum())
print("Exact repeated rows after first:", df.duplicated().sum())

# drop() here creates a temporary table; CustomerID remains in df and raw_df.
non_id_columns = df.columns.drop("CustomerID").tolist()
profile_repeats = df.duplicated(subset=non_id_columns)
print("Repeated profiles after first, excluding ID:", profile_repeats.sum())

# keep=False marks every member of a repeated-profile group. Save the mask
# for later review; avoid dumping hundreds of customer records to the screen.
all_repeated_profiles = df.duplicated(subset=non_id_columns, keep=False)
print("All rows belonging to repeated-profile groups:", all_repeated_profiles.sum())

# YOUR TURN: Inspect a small selection with df.loc[all_repeated_profiles].
# Can distinct customers legitimately share these measurements? What source
# evidence could establish whether these are independent observations?
# Resolve this before the later train/test split: related copies spanning
# both sets could make model evaluation overoptimistic.

# %% [markdown]
# ## 6. Inspect the target's overall balance
# This is a source audit, not analysis of relationships between predictors and
# Churn. The dictionary says only "Churn Flag"; confirm the 0/1 meaning before
# interpreting 1 as churned. Keep the literal labels in the output for now.

# %%
if df["Churn"].isna().any() or not df["Churn"].isin([0, 1]).all():
    raise ValueError("Churn must contain nonmissing 0/1 flags for this starter.")

target_summary = df["Churn"].value_counts().sort_index().rename("customers").to_frame()
target_summary["percent"] = target_summary["customers"].div(len(df)).mul(100).round(2)
print(target_summary.to_string())
print(f"Majority-label share (descriptive only): {target_summary['customers'].max() / len(df):.2%}")

# YOUR TURN: Why would accuracy alone be an incomplete measure later?
# This full-data share is NOT held-out baseline performance.

# %% [markdown]
# ## 7. Inspect category spellings and small coded scales
# dropna=False keeps missing categories visible if they occur. Two similar
# strings may mean the same thing, but similarity alone is not evidence.

# %%
for column in category_columns + ["CityTier", "SatisfactionScore", "Complain"]:
    print(f"\n{column}")
    print(df[column].value_counts(dropna=False).to_string())

# YOUR TURN: Investigate CC versus Credit Card, COD versus Cash on Delivery,
# Phone versus Mobile Phone, and Mobile versus Mobile Phone in order category.
# Record proposed mappings and evidence before writing replacement code.
# Do not globally replace words across columns; their meanings can differ.

# %% [markdown]
# ## 8. Inspect numeric ranges
# describe() reports nonmissing count, mean, standard deviation, quartiles,
# minimum, and maximum. .T puts one variable on each row for easier reading.
# Quartiles split the observed values into four parts. Missing values are
# omitted from these statistics, so check each column's count too.

# %%
numeric_summary = df[measurement_columns].describe().T
print(numeric_summary.round(2).to_string())

# Negative counts, durations, distances, or amounts merit investigation.
# This is a screening rule, not a complete proof that all values are valid.
negative_counts = df[measurement_columns].lt(0).sum()
print("\nNegative-value counts:")
print(negative_counts.to_string())

# YOUR TURN: Pick ONE measurement and fill in the commented template below.
# Use a column name from measurement_columns. Only remove the comments once
# you have replaced the placeholder. nlargest() inspects; it removes nothing.
# chosen_column = "REPLACE_WITH_A_COLUMN_NAME"
# print(df[["CustomerID", chosen_column]].nlargest(5, chosen_column))
# Write why the largest values might be legitimate, errors, or still unclear.

# %% [markdown]
# ## 9. Optional summary export
# False means no files are written when you run the starter normally. Switch
# to True to save three audit tables in reports/. Re-running then replaces
# these generated tables. The Excel workbook is never modified.

# %%
SAVE_SUMMARIES = False
if SAVE_SUMMARIES:
    reports_dir = PROJECT_DIR / "reports"
    reports_dir.mkdir(exist_ok=True)
    column_audit.to_csv(reports_dir / "column_audit.csv", index_label="column")
    target_summary.to_csv(reports_dir / "target_balance.csv", index_label="Churn")
    numeric_summary.to_csv(reports_dir / "numeric_summary.csv", index_label="column")
    print("Saved summary tables to:", reports_dir)

# %% [markdown]
# ## 10. Stop here and write your first observations
# Complete NOTES.md in your own words. Before exploring predictor-versus-Churn
# relationships, decide how repeated profiles will be handled and reserve an
# appropriate test set. Future imputation/scaling must be learned on training
# data only (and within each cross-validation training fold).
# K-means, a decision tree, and charts belong to later stages you can request.

# %%
# This check confirms that the provided inspection steps did not clean,
# filter, reorder, or otherwise alter the working data.
assert df.equals(raw_df), "The working data changed; review and document your edits."
print("\nFirst-look audit complete. Fill in NOTES.md before advancing.")
