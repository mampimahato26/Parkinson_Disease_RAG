import os
import sys
import time
import pandas as pd

# ======================================================
# Add Project Root
# ======================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.append(PROJECT_ROOT)

from src.rag_chat import ask_question

# ======================================================
# File Paths
# ======================================================

QUERY_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "Parkinson_Disease",
    "test_data",
    "queries.csv"
)

OUTPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "evaluation",
    "evaluation_results.csv"
)

# ======================================================
# Batch Settings
# Change only these two values
# ======================================================

START_INDEX = 180      # Question 1
END_INDEX = 280       # Question 20

# Examples:
# 20-40 -> START_INDEX=20 END_INDEX=40
# 40-60 -> START_INDEX=40 END_INDEX=60

# ======================================================
# Load Dataset
# ======================================================

df = pd.read_csv(QUERY_FILE)

df = df.iloc[START_INDEX:END_INDEX]

results = []

print("=" * 70)
print("Parkinson Disease RAG Evaluation")
print("=" * 70)
print(f"Evaluating Questions {START_INDEX+1} - {END_INDEX}")
print(f"Total Questions : {len(df)}")
print()

# ======================================================
# Evaluation Loop
# ======================================================

for index, row in df.iterrows():

    query_id = row["query_id"]
    question = row["question"]
    category = row["category"]
    expected_answer = row["expected_answer"]

    print(f"[{query_id}/200] {question}")

    success = False

    while not success:

        try:

            start = time.time()

            answer, sources = ask_question(question)

            end = time.time()

            response_time = round(end - start, 2)

            results.append({

                "query_id": query_id,
                "category": category,
                "question": question,
                "expected_answer": expected_answer,
                "generated_answer": answer,
                "response_time(sec)": response_time,
                "retrieved_source_count": len(sources),
                "retrieved_sources": " | ".join(sources)

            })

            print(f"✓ Completed ({response_time} sec)")
            print("-" * 70)

            success = True

            # small delay
            time.sleep(15)

        except Exception as e:

            error = str(e)

            if "429" in error or "RESOURCE_EXHAUSTED" in error:

                print("⚠ API quota exceeded.")
                print("Waiting 60 seconds...\n")

                time.sleep(60)

            else:

                print("❌ Error :", error)

                results.append({

                    "query_id": query_id,
                    "category": category,
                    "question": question,
                    "expected_answer": expected_answer,
                    "generated_answer": "ERROR",
                    "response_time(sec)": 0,
                    "retrieved_source_count": 0,
                    "retrieved_sources": ""

                })

                print("-" * 70)

                success = True

# ======================================================
# Save Results (Append Mode)
# ======================================================

results_df = pd.DataFrame(results)

# Create file with header if it doesn't exist or is empty.
# Otherwise append without header.
if (not os.path.exists(OUTPUT_FILE)) or (os.path.getsize(OUTPUT_FILE) == 0):

    results_df.to_csv(
        OUTPUT_FILE,
        mode="w",
        header=True,
        index=False,
        encoding="utf-8-sig"
    )

else:

    results_df.to_csv(
        OUTPUT_FILE,
        mode="a",
        header=False,
        index=False,
        encoding="utf-8-sig"
    )

print()
print("=" * 70)
print("Evaluation Completed Successfully")
print("=" * 70)
print(f"Results saved to: {OUTPUT_FILE}")
print(f"Questions saved: {START_INDEX + 1} - {END_INDEX}")