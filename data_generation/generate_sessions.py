import pandas as pd
import numpy as np
import random
from datetime import timedelta

# -----------------------------
# Config
# -----------------------------
USERS_FILE = "users_raw.csv"
SUBS_FILE = "subscriptions_raw.csv"
OUTPUT_FILE = "sessions_raw.csv"

random.seed(42)
np.random.seed(42)

# -----------------------------
# Load data
# -----------------------------
users = pd.read_csv(USERS_FILE, parse_dates=["signup_date"])
subs = pd.read_csv(SUBS_FILE, parse_dates=["start_date", "end_date"])

merged = subs.merge(
    users[["user_id", "signup_date"]],
    on="user_id",
    how="left"
)

device_types = ["web", "mobile", "tablet"]
device_probs = [0.65, 0.30, 0.05]

sessions = []
session_id = 1
today = pd.Timestamp.today()

# -----------------------------
# Generate sessions
# -----------------------------
for _, row in merged.iterrows():
    user_id = row["user_id"]
    plan = row["plan_type"]
    signup_date = row["signup_date"]
    end_date = row["end_date"]
    status = row["status"]

    # Determine base session count
    if pd.isna(plan):
        base_sessions = random.randint(3, 6)
    elif plan.lower() == "free":
        base_sessions = random.randint(8, 12)
    elif plan.lower() == "pro":
        base_sessions = random.randint(20, 35)
    else:
        base_sessions = random.randint(30, 50)

    # Reduce activity for churned users
    if status == "cancelled":
        base_sessions = int(base_sessions * 0.7)

    # Define observation window
    if status == "cancelled" and pd.notna(end_date):
        last_possible_date = min(end_date, today)
    else:
        last_possible_date = today

    # Safety check
    if last_possible_date <= signup_date:
        continue

    max_days = (last_possible_date - signup_date).days

    for _ in range(base_sessions):
        session_start = signup_date + timedelta(
            days=random.randint(0, max_days)
        )

        duration_min = random.randint(2, 45)
        session_end = session_start + timedelta(minutes=duration_min)

        device = np.random.choice(device_types, p=device_probs)

        sessions.append([
            session_id,
            user_id,
            session_start,
            session_end,
            device
        ])

        session_id += 1

sessions_df = pd.DataFrame(
    sessions,
    columns=[
        "session_id",
        "user_id",
        "session_start",
        "session_end",
        "device_type"
    ]
)

# -----------------------------
# Inject messiness (INTENTIONAL)
# -----------------------------

# Null session_end (~3%)
null_idx = sessions_df.sample(frac=0.03, random_state=1).index
sessions_df.loc[null_idx, "session_end"] = None

# Duplicate rows (~0.5%)
duplicates = sessions_df.sample(frac=0.005, random_state=2)
sessions_df = pd.concat([sessions_df, duplicates], ignore_index=True)

# Extremely long sessions (invalid)
long_idx = sessions_df.sample(frac=0.002, random_state=3).index
sessions_df.loc[long_idx, "session_end"] = (
    sessions_df.loc[long_idx, "session_start"] + timedelta(hours=5)
)

# Device casing inconsistency
sessions_df["device_type"] = sessions_df["device_type"].apply(
    lambda x: random.choice([x, x.upper(), x.capitalize()])
)

# -----------------------------
# Save
# -----------------------------
sessions_df.to_csv(OUTPUT_FILE, index=False)

print("sessions_raw.csv generated successfully")
print(sessions_df.head())
print("Total rows:", len(sessions_df))
