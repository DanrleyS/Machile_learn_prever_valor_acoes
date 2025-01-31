import os

# Executar a coleta de dados
print("\n📥 Coletando dados...")
os.system("python coletar_dados.py")

# Executar o pré-processamento
print("\n🔄 Pré-processando os dados...")
os.system("python processamento.py")

# Treinar o modelo
print("\n🤖 Treinando o modelo...")
os.system("python modelo.py")

# Fazer previsões
print("\n📊 Gerando previsões...")
os.system("python prever.py")

print("\n✅ Processo concluído com sucesso!")
