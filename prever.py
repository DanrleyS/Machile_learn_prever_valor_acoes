import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
import yfinance as yf

# Função para baixar dados de uma ação usando yfinance
def baixar_dados(ticker, inicio, fim):
    dados = yf.download(ticker, start=inicio, end=fim)
    return dados

# Baixar os dados históricos da PETR4
ticker = 'PETR4.SA'
dados = baixar_dados(ticker, '2024-01-01', '2025-01-31')

# Calcular as médias móveis de 20 e 50 períodos
dados['MM_20'] = dados['Close'].rolling(window=20).mean()
dados['MM_50'] = dados['Close'].rolling(window=50).mean()

# Remover valores NaN
dados.dropna(inplace=True)

# Exibir os dados após remoção dos NaNs
print("🔍 Dados Após Remover NaNs:")
print(dados[['Close', 'MM_20', 'MM_50']].tail())

# Normalizar os dados para a previsão
scaler = MinMaxScaler(feature_range=(0, 1))
dados_normalizados = scaler.fit_transform(dados[['Close', 'MM_20', 'MM_50']])

# Separando as variáveis independentes (X) e a variável dependente (y)
X = dados_normalizados[:, 1:]  # Usando MM_20 e MM_50
y = dados_normalizados[:, 0]  # Prevendo o preço de fechamento (Close)

# Dividir os dados em treino e teste
X_treino = X[:-1]  # Todos os dados menos o último
y_treino = y[:-1]
X_teste = X[-1:].reshape(1, -1)  # O último dado como teste

# Treinar o modelo de Regressão Linear
modelo = LinearRegression()
modelo.fit(X_treino, y_treino)

# Fazer a previsão para o último dia
previsoes_normalizadas = modelo.predict(X_teste)

# Reverter a normalização para obter os valores reais das previsões
dados_novos = dados.iloc[[-1]].copy()  # Última linha dos dados
previsoes = scaler.inverse_transform(np.concatenate([dados_novos[['MM_20', 'MM_50']].values, previsoes_normalizadas.reshape(-1, 1)], axis=1))[:, -1]

# Adicionar a previsão revertida aos dados
dados_novos['Previsao_Revertida'] = previsoes

# Exibir os dados após as previsões
print("🔍 Dados Após Previsões:")
print(dados_novos[['Close', 'Previsao_Revertida']])

# Resetar o índice para que 'Date' seja uma coluna normal
dados_novos_reset = dados_novos.reset_index()

# Plotar os resultados
plt.figure(figsize=(12, 6))

# Garantir que 'Date' seja convertida corretamente para datetime
dados_novos_reset['Date'] = pd.to_datetime(dados_novos_reset['Date'])

# Plotando as duas linhas: preço real e previsão revertida
plt.plot(dados['Close'], label="Preço Real", color="blue", linewidth=2)  # Preço Real
plt.scatter(dados_novos_reset["Date"], dados_novos_reset["Previsao_Revertida"], color="red", label="Previsão", zorder=5)  # Previsão

# Ajustar título e labels
plt.title(f"Previsão de Preço para {ticker}")
plt.xlabel("Data")
plt.ylabel("Preço (R$)")
plt.legend()
plt.grid()

# Ajustar a rotação das datas no eixo X para legibilidade
plt.xticks(rotation=45)

# Exibir gráfico
plt.tight_layout()
plt.show()

print("✅ Previsões geradas e exibidas no gráfico!")
