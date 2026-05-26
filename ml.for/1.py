import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
import xgboost as xgb

class KMeansHybridPredictor:
    def __init__(self, n_clusters=3):
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.xgb_model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
        
    def fit(self, X, y):
        clusters = self.kmeans.fit_predict(X)
        X_enhanced = X.copy()
        X_enhanced['Weather_Regime'] = clusters
        self.xgb_model.fit(X_enhanced, y)
        
    def predict(self, X):
        clusters = self.kmeans.predict(X)
        X_enhanced = X.copy()
        X_enhanced['Weather_Regime'] = clusters
        return self.xgb_model.predict(X_enhanced)

data = pd.read_csv('black_sea_waves_dataset.csv')

data['VHM0_yesterday'] = data['VHM0'].shift(1)
data['VTPK_yesterday'] = data['VTPK'].shift(1)
data['VMDR_yesterday'] = data['VMDR'].shift(1)
data = data.dropna()

X = data[['VHM0_yesterday', 'VTPK_yesterday', 'VMDR_yesterday']]
y = data['VHM0']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

model = KMeansHybridPredictor(n_clusters=3)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

mse = mean_squared_error(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)
print(f'Mean Squared Error: {mse:.4f}')
print(f'Mean Absolute Error: {mae:.4f}')

days = range(len(y_test))
plt.figure(figsize=(12, 6))

plt.plot(days, predictions,
         color='red', 
         linestyle=':', 
         linewidth=1, 
         label='Predicted Wave Height (m)')

plt.plot(days, y_test.values,
         color='blue', 
         linestyle='-', 
         linewidth=1, 
         alpha=0.7,
         label='Actual Wave Height (m)')

plt.title('Actual vs Predicted Wave Heights')
plt.xlabel('Hours in Test Period')
plt.ylabel('Significant Wave Height (VHM0)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.3)
plt.show()