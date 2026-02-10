import pandas as pd
import numpy as np
import random
from datetime import timedelta

# -----------------------------
# Config
# -----------------------------
USERS_FILE = "users_raw.csv"
SUBS_FILE = "subscriptions_raw.csv"
OUTPUT_FILE = "feedback_raw.csv"

random.seed(42)
np.random.seed(42)

# -----------------------------
# Load data
# -----------------------------
users = pd.read_csv(USERS_FILE, parse_dates=["signup_date"])
subs = pd.read_csv(SUBS_FILE, parse_dates=["start_date", "end_date"])

df = users.merge(
    subs[["user_id", "plan_type", "status", "end_date"]],
    on="user_id",
    how="left"
)

# -----------------------------
# Feedback generation
# -----------------------------
feedback_rows = []
feedback_id = 1

for _, row in df.iterrows():
    user_id = row["user_id"]
    signup_date = row["signup_date"]
    plan = row["plan_type"]
    status = row["status"]
    end_date = row["end_date"]

    # Decide if user gives feedback
    if pd.isna(plan):
        give_feedback = random.random() < 0.20
    elif plan.lower() == "free":
        give_feedback = random.random() < 0.30
    else:
        give_feedback = random.random() < 0.45

    if not give_feedback:
        continue

    # Rating logic
    if status == "cancelled":
        rating = np.random.choice([1, 2, 3], p=[0.45, 0.35, 0.20])
    elif isinstance(plan, str) and plan.lower() in ["pro", "team"]:
        rating = np.random.choice([4, 5], p=[0.4, 0.6])
    else:
        rating = np.random.choice([3, 4, 5], p=[0.4, 0.4, 0.2])

    comments = {
        1: ["bad experience", "very slow", "not useful"],
        2: ["needs improvement", "too many bugs"],
        3: ["okay", "average experience"],
        4: ["good tool", "helpful features"],
        5: ["excellent", "very useful", "love it"]
    }

    comment = random.choice(comments.get(rating, ["okay"]))

    # Feedback date
    if status == "cancelled" and pd.notna(end_date):
        feedback_date = signup_date + timedelta(
            days=random.randint(5, max(5, (end_date - signup_date).days))
        )
    else:
        feedback_date = signup_date + timedelta(
            days=random.randint(5, 300)
        )

    feedback_rows.append([
        feedback_id,
        user_id,
        rating,
        comment,
        feedback_date
    ])

    feedback_id += 1

feedback_df = pd.DataFrame(
    feedback_rows,
    columns=["feedback_id", "user_id", "rating", "comment", "feedback_date"]
)

# -----------------------------
# Inject messiness
# -----------------------------

# Null comments (~5%)
null_idx = feedback_df.sample(frac=0.05, random_state=1).index
feedback_df.loc[null_idx, "comment"] = None

# Invalid ratings (~2%)
bad_rating_idx = feedback_df.sample(frac=0.02, random_state=2).index
feedback_df.loc[bad_rating_idx, "rating"] = np.random.choice([0, 6])

# Duplicate rows (~1%)
duplicates = feedback_df.sample(frac=0.01, random_state=3)
feedback_df = pd.concat([feedback_df, duplicates], ignore_index=True)

# Comment casing inconsistency
feedback_df["comment"] = feedback_df["comment"].apply(
    lambda x: random.choice([x, str(x).upper(), str(x).lower()]) if pd.notna(x) else x
)

# -----------------------------
# Save
# -----------------------------
feedback_df.to_csv(OUTPUT_FILE, index=False)

print("feedback_raw.csv generated successfully")
print(feedback_df.head())
print("Total rows:", len(feedback_df))
