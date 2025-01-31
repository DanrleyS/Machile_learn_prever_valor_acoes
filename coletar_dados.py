import yfinance as yf
import pandas as pd

# Defina o ticker da ação (exemplo: PETR4.SA)
ticker = "PETR4.SA"

# Baixar os dados históricos (por exemplo, últimos 5 anos)
dados = yf.download(ticker, start="2020-01-01", end="2025-01-01")

# Exibir as colunas para diagnóstico
print("🔍 Colunas do DataFrame antes da renomeação:", dados.columns)

# Aplanar o MultiIndex para obter um índice simples
dados.columns = dados.columns.get_level_values(0)

# Exibir as colunas após a aplanada
print("🔍 Colunas do DataFrame após aplanamento:", dados.columns)

# Garantir que o índice de datas seja transformado em uma coluna
dados.reset_index(inplace=True)  # Reseta o índice para que 'Date' se torne uma coluna

# Adicionar a coluna "Adj Close" manualmente, se necessário
if "Adj Close" not in dados.columns:
    dados["Adj Close"] = dados["Close"]

# Verificar as colunas novamente após a adição
print("🔍 Colunas do DataFrame após adicionar 'Adj Close':", dados.columns)

# Renomear as colunas conforme necessário
if len(dados.columns) == 7:
    dados.columns = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
else:
    print(f"⚠️ O número de colunas não corresponde a 7. O DataFrame tem {len(dados.columns)} colunas.")
    print("🔍 Colunas atuais:", dados.columns)

# Salvar os dados no arquivo CSV, se a renomeação for bem-sucedida
if len(dados.columns) == 7:
    dados.to_csv("dados_brutos.csv", index=False)
    print("✅ Dados coletados e salvos em 'dados_brutos.csv'")
