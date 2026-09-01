import os
import pandas as pd

# ======================================================
# Project Root
# ======================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

# ======================================================
# File Paths
# ======================================================

INPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "evaluation",
    "evaluation_results.csv"
)

OUTPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "evaluation",
    "performance_metrics.csv"
)

# ======================================================
# Load Evaluation Results
# ======================================================

df = pd.read_csv(INPUT_FILE)

# Replace missing answers with empty string
df["generated_answer"] = df["generated_answer"].fillna("")

# ======================================================
# Calculate Metrics
# ======================================================

total_questions = len(df)

# Failed Responses
failed = len(
    df[
        (df["generated_answer"] == "ERROR") |
        (
            df["generated_answer"].str.contains(
                "I could not find sufficient information",
                case=False,
                na=False
            )
        )
    ]
)

# Successful Responses
successful = total_questions - failed

# Rates
success_rate = round((successful / total_questions) * 100, 2)
failure_rate = round((failed / total_questions) * 100, 2)

# Response Time Statistics
avg_response = round(df["response_time(sec)"].mean(), 2)
min_response = round(df["response_time(sec)"].min(), 2)
max_response = round(df["response_time(sec)"].max(), 2)

# Retrieved Source Statistics
avg_sources = round(df["retrieved_source_count"].mean(), 2)
min_sources = int(df["retrieved_source_count"].min())
max_sources = int(df["retrieved_source_count"].max())

# ======================================================
# Save Metrics
# ======================================================

metrics = [
    ["Total Questions", total_questions],
    ["Successful Responses", successful],
    ["Failed Responses", failed],
    ["Success Rate (%)", success_rate],
    ["Failure Rate (%)", failure_rate],
    ["Average Response Time (sec)", avg_response],
    ["Minimum Response Time (sec)", min_response],
    ["Maximum Response Time (sec)", max_response],
    ["Average Retrieved Sources", avg_sources],
    ["Minimum Retrieved Sources", min_sources],
    ["Maximum Retrieved Sources", max_sources]
]

metrics_df = pd.DataFrame(
    metrics,
    columns=["Metric", "Value"]
)

metrics_df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

# ======================================================
# Print Results
# ======================================================

print("=" * 60)
print("Performance Metrics Generated Successfully")
print("=" * 60)

print(f"Total Questions           : {total_questions}")
print(f"Successful Responses      : {successful}")
print(f"Failed Responses          : {failed}")
print(f"Success Rate              : {success_rate}%")
print(f"Failure Rate              : {failure_rate}%")
print(f"Average Response Time     : {avg_response} sec")
print(f"Minimum Response Time     : {min_response} sec")
print(f"Maximum Response Time     : {max_response} sec")
print(f"Average Retrieved Sources : {avg_sources}")
print(f"Minimum Retrieved Sources : {min_sources}")
print(f"Maximum Retrieved Sources : {max_sources}")

print()
print(f"Saved to: {OUTPUT_FILE}")