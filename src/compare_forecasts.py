from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing


BASE = Path(__file__).resolve().parents[1]
DATA_PATH = BASE / "data" / "ecommerce_orders.csv"
REPORT_PATH = BASE / "reports" / "forecast_model_comparison.csv"


def calculate_metrics(actual, predicted):
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)

    mae = np.mean(np.abs(actual - predicted))
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100

    return {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape,
    }


# --------------------------------------------------
# 1. Load data
# --------------------------------------------------

df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])

monthly = (
    df.set_index("order_date")
    .resample("MS")["revenue"]
    .sum()
)

print("Total months:", len(monthly))
print("Date range:", monthly.index.min().date(), "to", monthly.index.max().date())


# --------------------------------------------------
# 2. Train / test split
# Last 6 months are kept completely unseen
# --------------------------------------------------

train = monthly.iloc[:-6]
test = monthly.iloc[-6:]

print("\nTraining months:", len(train))
print("Test months:", len(test))

print("\nTest period:")
print(test.round(2).to_string())


# --------------------------------------------------
# 3. Naive forecast
# Forecast every test month using last training value
# --------------------------------------------------

naive_pred = np.repeat(train.iloc[-1], len(test))


# --------------------------------------------------
# 4. Seasonal Naive
# Same calendar month from previous year
# --------------------------------------------------

seasonal_naive_pred = monthly.shift(12).loc[test.index].values


# --------------------------------------------------
# 5. 3-month Moving Average
# Recursive forecast
# --------------------------------------------------

history = list(train.values)
moving_average_pred = []

for _ in range(len(test)):
    prediction = np.mean(history[-3:])
    moving_average_pred.append(prediction)
    history.append(prediction)


# --------------------------------------------------
# 6. Holt-Winters
# --------------------------------------------------

hw_model = ExponentialSmoothing(
    train,
    trend="add",
    seasonal="add",
    seasonal_periods=12,
).fit()

hw_pred = hw_model.forecast(len(test)).values


# --------------------------------------------------
# 7. Evaluate all models
# --------------------------------------------------

predictions = {
    "Naive": naive_pred,
    "Seasonal Naive": seasonal_naive_pred,
    "3-Month Moving Average": moving_average_pred,
    "Holt-Winters": hw_pred,
}

results = []

for model_name, prediction in predictions.items():
    metrics = calculate_metrics(test.values, prediction)

    results.append(
        {
            "Model": model_name,
            "MAE": metrics["MAE"],
            "RMSE": metrics["RMSE"],
            "MAPE": metrics["MAPE"],
        }
    )


results_df = pd.DataFrame(results)
results_df = results_df.sort_values("MAPE").reset_index(drop=True)

print("\nMODEL COMPARISON")
print("=" * 65)

print(
    results_df.to_string(
        index=False,
        formatters={
            "MAE": "{:.2f}".format,
            "RMSE": "{:.2f}".format,
            "MAPE": "{:.2f}%".format,
        },
    )
)


# --------------------------------------------------
# 8. Best model
# --------------------------------------------------

best_model = results_df.iloc[0]["Model"]

print("\nBest model based on lowest MAPE:")
print(best_model)


# --------------------------------------------------
# 9. Detailed predictions
# --------------------------------------------------

comparison = pd.DataFrame(
    {
        "Actual": test.values,
        "Naive": naive_pred,
        "Seasonal_Naive": seasonal_naive_pred,
        "Moving_Average": moving_average_pred,
        "Holt_Winters": hw_pred,
    },
    index=test.index,
)

print("\nACTUAL VS PREDICTED")
print("=" * 90)
print(comparison.round(2).to_string())


# --------------------------------------------------
# 10. Save model comparison
# --------------------------------------------------

results_df.to_csv(REPORT_PATH, index=False)

print("\nSaved:")
print(REPORT_PATH)