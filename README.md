# E-commerce customer churn: a guided starting point

This is the foundation for your own analysis. It loads your actual workbook,
checks its structure and quality, and gives you small exercises to complete.
The analysis code uses only **pandas** and **openpyxl**, plus Python's built-in
`pathlib`. No models, plotting libraries, automatic cleaning, or feature
engineering have been added.

The working project question from your earlier chat is:

> How does churn vary across e-commerce customer segments, and how can a churn
> model help prioritize retention outreach for each group?

The eventual methods are k-means for customer segments and a decision tree for
the recorded churn outcome, provided both satisfy your course requirements.
Your current milestone is simpler: explain the dataset, identify its problems,
and document what needs to happen before modeling. A strong project begins
with defensible choices, not a large collection of libraries.

## What is included

```text
ecommerce_churn_starter/
  README.md                    This guide and run instructions
  starter_analysis.py          Working code with explanations and exercises
  starter_analysis.ipynb       The same starting code, divided into cells
  requirements.txt             Two direct dependencies, pinned to tested versions
  DATA_DICTIONARY.md           All 20 columns and unresolved definitions
  NOTES.md                     Your observations and decision log
  .gitignore                   Keeps generated files and local raw data out of Git
  data/raw/E Commerce Dataset.xlsx
```

The workbook is an unchanged copy extracted from your supplied archive. Your
original ZIP and PDF were not edited. The script and notebook are alternative
ways to start: choose one to edit. They do not synchronize automatically.
The notebook intentionally has no saved results; generate them yourself by
running the cells. Keep your code, data, and notes together when moving folders.

## Get it running on Windows

Use an existing compatible Python environment if you already have one. The
pinned pandas version requires Python 3.11 or newer. The supplied code was
validated with pandas 3.0.1 and openpyxl 3.1.5 using the available bundled runtime.

Otherwise, open PowerShell **inside this project folder** and run these commands
one at a time:

```powershell
py --version
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe starter_analysis.py
```

- `py --version` tells you which Python the Windows launcher selects.
- `venv` makes a local environment named `.venv`, keeping project dependencies
  separate from other projects.
- `-m pip` runs the installer belonging to that environment. The requirements
  file requests just the two direct libraries; pip also installs their required
  dependencies, such as NumPy for pandas.
- The final command runs the script from beginning to end and prints tables.
  No environment activation or PowerShell execution-policy change is needed.

If `py` is unavailable but `python --version` works, replace `py` with `python`
in the first two commands. In an editor, select this project's `.venv` Python
as the interpreter so that running the file uses the same installed packages.

For the notebook, use your existing Jupyter-capable environment and select a
kernel with these dependencies. Open it from this project folder and run cells
in order. Notebook tooling is not included in requirements because it is not
needed to run the script. If you do not already use notebooks, start with the
script; it provides the same code without additional setup.

Common errors:

| Message | Likely cause and fix |
|---|---|
| No module named pandas | Install the requirements using the Python interpreter running your code. |
| Missing optional dependency openpyxl | Install requirements; pandas uses openpyxl to read this Excel file. |
| Workbook not found | Keep `data/raw` beside the code. A notebook's working directory must be this project folder. |
| Worksheet not found | Check the workbook and exact sheet name: `E Comm`, including the space. |
| NameError in a notebook | An earlier cell was skipped or the kernel restarted. Run from the beginning. |

## What the code does, step by step

### 1. Set up paths and tools

`Path` builds file paths without hardcoding your Downloads folder. The script
locates data relative to its own file. A notebook uses its working directory.
The existence check gives a helpful error before trying to read a missing file.
`import pandas as pd` gives pandas the conventional short name `pd`.

### 2. Load the workbook correctly

The workbook has two sheets: `Data Dict` and `E Comm`. Reading the first sheet
by default would load descriptions instead of customer observations. The code
explicitly names both sheets. The dictionary has a blank first Excel row, so
`header=1` uses its second row as column headings. Python counts from zero.

`raw_df` is the source table in memory. `df = raw_df.copy(deep=True)` creates a
separate working table. Later edits to `df` should leave `raw_df` unchanged.
`shape` gives row and column counts; `head()` previews five rows. The preview
is for checking the load, not a random or representative sample.

See pandas' [read_excel documentation](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html)
for sheet selection and header handling.

### 3. Separate storage types from analytical meaning

`info()` prints column types and nonmissing counts. A `float64` count can simply
reflect missing values, not fractional customers or orders. `CustomerID` is
stored as a number, but averaging it has no business meaning. `CityTier` is a
code; its numerical distances do not automatically represent equally spaced
differences. The lists in the script organize inspection, not model selection.

Read DATA_DICTIONARY.md before interpreting any column. In particular,
`CashbackAmount` is described as average cashback in the last month; it is not
documented revenue, customer lifetime value, or total spending.

### 4. Measure missingness before deciding what to do

The audit shows type, missing count, missing percentage, and distinct-value
count for every column. `isna()` creates a table of True/False values; summing
those flags counts missing cells. Their mean is the missing fraction.
`any(axis=1)` checks whether each row has at least one missing cell.

The starter never fills missing values. Zero is a real value for fields such
as coupons and tenure; replacing unknown values with zero would make a claim
the source does not support. Dropping every incomplete row can remove a large
portion of the data and change the population you analyze.

See pandas' [missing-data guide](https://pandas.pydata.org/docs/user_guide/missing_data.html)
for how missing values are represented and detected.

### 5. Distinguish three duplicate questions

The script checks repeated full rows, repeated customer IDs, and repeated
profiles after excluding the ID. These answer different questions. Distinct
IDs do not establish that observations are independent, while matching values
do not prove that two customers are the same person.

`duplicated()` marks repeats after the first occurrence. `keep=False` instead
marks every row in a repeated group. This difference matters when reporting
counts. Investigate source provenance before deleting records or choosing a
split. If repeated profiles are copied observations, letting related copies
land in both training and test data could make evaluation too optimistic.
If they are legitimately independent customers, removing them may discard
real observations. The starter flags the question without choosing for you.

### 6. Check the target balance

`value_counts()` counts the two recorded Churn labels. Dividing by the total
row count gives their proportions. The code validates nonmissing 0/1 values,
but this does not establish what the labels mean. The supplied dictionary says
only “Churn Flag.” Treat 1=churned as a working assumption until you document
confirmation. No future prediction window is established by that description.

The largest class represents 83.16% of this supplied file. That illustrates
why accuracy alone can be misleading: always choosing the common label would
already match many records. This is a descriptive full-data share, **not** a
measured test-set baseline. Actual model evaluation belongs to a later stage.

### 7. Review category labels

The loop prints one frequency table per category or coded scale, including
missing values if present. Look for plausible synonyms such as `CC` and
`Credit Card`, but record the evidence before merging. `Phone` could mean
something different from `Mobile Phone`; similar spelling is insufficient.
Keep mappings specific to a column and preserve the original raw data.

### 8. Inspect ranges without deleting extremes

`describe().T` puts each measurement on a row with its nonmissing count, mean,
standard deviation, quartiles, minimum, and maximum. The negative-value screen
is an initial plausibility check. Passing it does not prove the data is valid.

For your first code exercise, choose one column and complete the commented
`nlargest()` example. Inspect the records with its largest values. Ask what
units, source details, or related measurements would help explain them. A large
value is not automatically an error, and zero is not automatically missing.
These checks are for discovering questions; do not tune cutoff rules using
the full dataset before reserving evaluation data.

### 9. Save only when useful

`SAVE_SUMMARIES = False` keeps normal execution read-only. Setting it to True
saves the column audit, target balance, and numeric summary as CSV tables in
`reports/`. Those generated tables are replaced on subsequent export runs.
The source Excel workbook is never written. These exports are summaries,
not a cleaned dataset. Keep your original reasoning in NOTES.md.

### 10. Verify and pause

The final assertion checks that the working table still equals the raw table.
If you later add cleaning, this assertion should be reconsidered and replaced
with checks appropriate to your documented changes. For now, a successful run
means the inspection code completed; it does not certify the data as clean.

## Findings verified in your supplied file

| Check | Result |
|---|---:|
| Customer-sheet rows | 5,630 |
| Columns | 20 |
| Missing IDs / repeated IDs / exact repeated full rows | 0 / 0 / 0 |
| Repeated profiles excluding ID, after first occurrence | 556 |
| Churn flag 0 | 4,682 (83.16%) |
| Churn flag 1 | 948 (16.84%) |
| Rows with at least one missing value | 1,856 (32.97%) |
| Rows remaining after dropping all incomplete rows | 3,774 |

| Column with missing values | Count | Percent of rows |
|---|---:|---:|
| DaySinceLastOrder | 307 | 5.45% |
| OrderAmountHikeFromlastYear | 265 | 4.71% |
| Tenure | 264 | 4.69% |
| OrderCount | 258 | 4.58% |
| CouponUsed | 256 | 4.55% |
| HourSpendOnApp | 255 | 4.53% |
| WarehouseToHome | 251 | 4.46% |

Potential category overlaps occur in payment mode, login device, and preferred
order category. Numeric maxima such as 127 for `WarehouseToHome` and 61 for
`Tenure` deserve context; their units are not provided in the local dictionary.
No values have been corrected, removed, imputed, or renamed.

## Your first working session

1. Run the complete starter once and compare the output with the checks above.
2. Rerun sections individually and explain each output in your own words.
3. Fill in the problem statement and definition gaps in NOTES.md.
4. Complete the one-column extreme-value exercise yourself.
5. Record at least three unresolved decisions, including repeated profiles.
6. Write two questions you want later exploration to answer.

You are ready to move on when you can explain one row, distinguish an ID from
a measurement, quantify missingness, describe the target balance, and justify
why the flagged issues need investigation. You do not need to solve every
cleaning issue in this first session.

## The next stages, when you request them

Before comparing predictors against churn, resolve the row-independence issue
and reserve test data. An ordinary stratified split may fit independent
customer observations; related copies require a different decision, such as
grouping related records. Do not choose a split strategy solely for higher
scores. Keep later exploratory relationships and model choices on training data.

Missing-value replacements, scaling statistics, and other learned
preprocessing must be estimated on training data and within each training
fold during cross-validation. See the official
[data-leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage).
This starter deliberately does not implement a split or preprocessing yet.

Later you can add a few focused plots, numerical behavioral clustering that
excludes ID and Churn, and one decision tree compared with a simple baseline.
Choose and interpret clusters from behavior before comparing their churn
rates. Cross-validation and confusion matrices assess models; they are not
substitutes for the two substantive analytics methods. Ultimately connect
findings to proposed retention actions that would need testing. This dataset
alone cannot establish that an action causes improved retention or that your
method generalizes to multiple businesses.

## Assignment context and ownership

The supplied two-page assignment calls for original individual work, at least
two analytics methods covered in class, commented `.py` and/or `.ipynb` code,
a report PDF, and presentation slides in PDF. It asks you to disclose methods
or libraries not covered in class and cite open-source code. Those are course
requirements to plan around; they do not expand this request into a completed
project. This starter is not a submission-ready report or presentation.

Keep the judgments, implementation exercises, interpretation, and final
writing your own. The assistance entry in NOTES.md identifies what was
provided so you can maintain an honest record. Check your instructor's actual
assistance policy if needed; the supplied PDF does not give a specific AI rule.

Sources: the workbook's `Data Dict` and `E Comm` sheets; your supplied
`Final Project (1).pdf`, pages 1-2; your linked earlier chat; and the official
documentation linked beside the relevant explanations. The original Kaggle
URL is recorded in NOTES.md; dataset provenance and redistribution terms
still need your review before publishing data with a resume project.
