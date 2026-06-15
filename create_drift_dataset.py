import pandas as pd

df = pd.read_csv("data/aml_test.csv")

# Introduce drift
df["TransactionAmount"] = df["TransactionAmount"] * 15

df["TransactionsPerDay"] = (
    df["TransactionsPerDay"] * 8
)

df["CountryRiskScore"] = (
    df["CountryRiskScore"] * 0.2
)

df.to_csv(
    "data/aml_drift.csv",
    index=False
)

print("Drift dataset created")
print(df.head())
