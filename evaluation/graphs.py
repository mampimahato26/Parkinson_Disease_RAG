import os
import pandas as pd
import matplotlib.pyplot as plt

# ======================================================
# Project Root
# ======================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

# ======================================================
# Paths
# ======================================================

INPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "evaluation",
    "evaluation_results.csv"
)

GRAPH_FOLDER = os.path.join(
    PROJECT_ROOT,
    "evaluation",
    "graphs"
)

os.makedirs(GRAPH_FOLDER, exist_ok=True)

# ======================================================
# Load CSV
# ======================================================

df = pd.read_csv(INPUT_FILE)

# ======================================================
# Evaluation Logic
# ======================================================

failed_mask = (
    (df["generated_answer"] == "ERROR") |
    (
        df["generated_answer"]
        .str.contains(
            "I could not find sufficient information",
            case=False,
            na=False
        )
    )
)

successful = len(df[~failed_mask])
failed = len(df[failed_mask])

# ======================================================
# Graph 1 : Success vs Failed
# ======================================================

plt.figure(figsize=(6,6))

plt.pie(
    [successful, failed],
    labels=["Successful", "Failed"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Response Success Distribution")

plt.savefig(
    os.path.join(
        GRAPH_FOLDER,
        "success_vs_failed.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ======================================================
# Graph 2 : Response Time Distribution
# ======================================================

plt.figure(figsize=(8,5))

plt.hist(
    df["response_time(sec)"],
    bins=20
)

plt.xlabel("Response Time (sec)")
plt.ylabel("Frequency")
plt.title("Response Time Distribution")

plt.savefig(
    os.path.join(
        GRAPH_FOLDER,
        "response_time_distribution.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ======================================================
# Graph 3 : Questions per Category
# ======================================================

category_count = (
    df["category"]
    .value_counts()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10,6))

category_count.plot(kind="bar")

plt.xlabel("Category")
plt.ylabel("Number of Questions")
plt.title("Questions per Category")

plt.xticks(rotation=45, ha="right")

plt.tight_layout()

plt.savefig(
    os.path.join(
        GRAPH_FOLDER,
        "questions_per_category.png"
    ),
    dpi=300
)

plt.close()

# ======================================================
# Graph 4 : Retrieved Sources Distribution
# ======================================================

plt.figure(figsize=(8,5))

plt.hist(
    df["retrieved_source_count"],
    bins=10
)

plt.xlabel("Retrieved Sources")
plt.ylabel("Frequency")
plt.title("Retrieved Sources Distribution")

plt.savefig(
    os.path.join(
        GRAPH_FOLDER,
        "retrieved_sources_distribution.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ======================================================
# Graph 5 : Average Response Time
# ======================================================

average_time = df["response_time(sec)"].mean()

plt.figure(figsize=(5,5))

plt.bar(
    ["Average"],
    [average_time]
)

plt.ylabel("Seconds")
plt.title("Average Response Time")

plt.savefig(
    os.path.join(
        GRAPH_FOLDER,
        "average_response_time.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ======================================================
# Done
# ======================================================

print("="*60)
print("Graphs Generated Successfully")
print("="*60)
print(f"Successful Responses : {successful}")
print(f"Failed Responses     : {failed}")
print(f"Success Rate         : {successful/len(df)*100:.2f}%")
print()
print(f"Graphs saved in : {GRAPH_FOLDER}")