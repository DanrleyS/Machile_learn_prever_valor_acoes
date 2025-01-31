import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
from sklearn.preprocessing import MinMaxScaler

# Carregar os dados pré-processados
X_train_scaled = pd.read_csv("X_train_scaled.csv", index_col=0)
X_test_scaled = pd.read_csv("X_test_scaled.csv", index_col=0)
y_train = pd.read_csv("y_train.csv", index_col=0)
y_test = pd.read_csv("y_test.csv", index_col=0)

# Criar e treinar o modelo de regressão linear
modelo = LinearRegression()
modelo.fit(X_train_scaled, y_train)

# Avaliação do modelo
mae = mean_absolute_error(y_test, modelo.predict(X_test_scaled))
rmse = np.sqrt(mean_squared_error(y_test, modelo.predict(X_test_scaled)))

print(f"✅ Modelo treinado!")
print(f"📊 Erro Médio Absoluto (MAE): {mae:.4f}")
print(f"📉 Raiz do Erro Quadrático Médio (RMSE): {rmse:.4f}")

# Criar e salvar o scaler
scaler = MinMaxScaler()
scaler.fit(X_train_scaled)  # Ajuste do scaler nos dados de treino
joblib.dump(scaler, "scaler.pkl")

# Salvar o modelo treinado
joblib.dump(modelo, "modelo_regressao.pkl")

print("✅ Modelo e scaler salvos como 'modelo_regressao.pkl' e 'scaler.pkl'")
