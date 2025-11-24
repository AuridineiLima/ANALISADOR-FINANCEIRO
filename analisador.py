import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# ===========================
#  Funções de apoio
# ===========================

def tratar_ticker(ticker):
    """
    Converte automaticamente ativos da B3 (ex: PETR4 → PETR4.SA)
    """
    ticker = ticker.upper().strip()
    if ticker[-1].isdigit() and ".SA" not in ticker:
        return ticker + ".SA"
    return ticker

def escolher_periodo():
    print("\nEscolha o período:")
    print("1 - 1 ano")
    print("2 - 3 anos")
    print("3 - 5 anos")
    print("4 - Personalizado")
    
    opc = input("Opção: ")

    if opc == "1":
        return ("2024-01-01", "2025-01-01")
    elif opc == "2":
        return ("2022-01-01", "2025-01-01")
    elif opc == "3":
        return ("2020-01-01", "2025-01-01")
    elif opc == "4":
        inicio = input("Data inicial (YYYY-MM-DD): ")
        fim = input("Data final   (YYYY-MM-DD): ")
        return (inicio, fim)
    else:
        print("Opção inválida. Usando padrão: 2020 → 2025.")
        return ("2020-01-01", "2025-01-01")


# ===========================
#  Início do aplicativo
# ===========================

print("=== Analisador Financeiro com Python ===")

ticker_usuario = input("Digite o ticker (ex: PETR4, VALE3, AAPL): ")

ticker_final = tratar_ticker(ticker_usuario)
print("Ticker convertido:", ticker_final)

data_inicio, data_fim = escolher_periodo()

print(f"\nBaixando dados de {ticker_final}...")
dados = yf.download(ticker_final, start=data_inicio, end=data_fim)

if dados.empty:
    print("Erro: nenhum dado encontrado para esse ticker.")
    exit()

# ===========================
#  Cálculos financeiros
# ===========================

# Retorno diário
dados["Retorno"] = dados["Close"].pct_change()

# Retorno acumulado
dados["RetAcumulado"] = (1 + dados["Retorno"]).cumprod() - 1

# Médias móveis
dados["MM20"] = dados["Close"].rolling(window=20).mean()     # curto prazo
dados["MM50"] = dados["Close"].rolling(window=50).mean()     # médio prazo


# ===========================
#  Gráficos
# ===========================

# ----- Gráfico 1: Preço + Médias -----
plt.figure(figsize=(12, 6))
plt.plot(dados["Close"], label="Preço")
plt.plot(dados["MM20"], label="MM20", linestyle='--')
plt.plot(dados["MM50"], label="MM50", linestyle='--')

plt.title(f"{ticker_final} - Preço + Médias Móveis")
plt.xlabel("Data")
plt.ylabel("Preço")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# ----- Gráfico 2: Retorno Acumulado -----
plt.figure(figsize=(12, 5))
plt.plot(dados["RetAcumulado"], label="Retorno Acumulado")
plt.title(f"{ticker_final} - Retorno Acumulado")
plt.xlabel("Data")
plt.ylabel("Retorno")
plt.grid(True)
plt.tight_layout()
plt.show()


# ----- Gráfico 3: Retorno Diário -----
plt.figure(figsize=(12, 5))
plt.plot(dados["Retorno"], label="Retorno Diário")
plt.title(f"{ticker_final} - Retorno Diário")
plt.xlabel("Data")
plt.ylabel("Retorno")
plt.grid(True)
plt.tight_layout()
plt.show()

print("\nAnálise concluída!")
