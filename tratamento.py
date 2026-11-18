import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

df = pd.read_csv("data/raw/dados_brutos.csv")
df = df.dropna(subset=["Poluente_PM25", "Poluente_NO2"]).copy()

df["Data"] = pd.to_datetime(df["Data_Hora"]).dt.date.astype(str)
df_diario = (
    df.groupby(["Data", "Cidade", "Regiao"], as_index=False)
    .agg({"Poluente_PM25": "mean", "Poluente_NO2": "mean"})
)

df_diario["Poluente_PM25"] = df_diario["Poluente_PM25"].round(2)
df_diario["Poluente_NO2"] = df_diario["Poluente_NO2"].round(2)

def categorizar_qualidade(pm25):
    if pm25 <= 15: return "Boa"
    elif pm25 <= 35: return "Moderada"
    else: return "Ruim"

df_diario["Status_Qualidade"] = df_diario["Poluente_PM25"].apply(categorizar_qualidade)

fator_cidade = {
    "Jundiaí": 3.2, "Várzea Paulista": 1.8, "Campo Limpo Paulista": 1.5,
    "Caieiras": 2.1, "Franco da Rocha": 2.8, "Francisco Morato": 3.0
}
df_diario["Casos_Respiratorios_Est"] = (
    df_diario["Poluente_PM25"] * df_diario["Cidade"].map(fator_cidade)
).round().astype(int)

df_diario.to_csv("data/processed/dados_tratados.csv", index=False)
print("2. Dados tratados salvos!")
