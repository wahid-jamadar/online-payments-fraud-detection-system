import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load Dataset
print("Phase-1 Loading dataset...")
df = pd.read_csv("data/PS_20174392719_1491204439457_log.csv")

# Keep needed columns
df = df[
    [
        "step",
        "type",
        "amount",
        "oldbalanceOrg",
        "newbalanceOrig",
        "oldbalanceDest",
        "newbalanceDest",
        "isFraud"
    ]
]

print("Phase-2 Preprocessing data...")

# Encode type column
encoder = LabelEncoder()
df["type"] = encoder.fit_transform(df["type"])

# Features / target
X = df.drop("isFraud", axis=1)
y = df["isFraud"]

# Split
print("Phase-3 Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
print("Phase-4 Training model...")
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=12,
    random_state=42
)

model.fit(X_train, y_train)

# Test
print("Phase-5 Evaluating model...")
pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)

print("Accuracy:", acc)
print(classification_report(y_test, pred))

# Save model + encoder
print("Phase-6 Saving model...")
joblib.dump(model, "model/fraud_model.pkl")
joblib.dump(encoder, "model/label_encoder.pkl")


print("Last Phase Model saved successfully.")