# 🚦 Monitoramento de Tráfego em São Paulo — Dashboard em Tempo Real

Este projeto realiza a **coleta automática de dados de tráfego da cidade de São Paulo** utilizando a **API TomTom**, armazena os dados em **CSV**, realiza **tratamento e análise**, e apresenta os resultados em um **dashboard interativo desenvolvido com Streamlit**.

---

## 📌 Objetivo

Criar uma solução que permita monitorar o trânsito em São Paulo em tempo real, analisando:
- Congestionamentos
- Velocidade do fluxo
- Índice de fluidez
- Variações ao longo do tempo

O projeto pode ser utilizado para fins de estudo, análise urbana, mobilidade, segurança pública e planejamento de rotas.

---

## 🧠 Tecnologias utilizadas

| Categoria | Ferramenta |
|----------|------------|
| Linguagem | Python |
| Dados | Pandas, CSV |
| Visualização | Streamlit, Plotly |
| Coleta | API TomTom |
| Automatização | Agendamento via Script / Cron (opcional) |

---

## 📂 Estrutura do Projeto

📁 trafego_carros
├── coleta_trafego_sp.py # Coleta dados via API TomTom
├── limpeza_trafego.py # Tratamento e preparação dos dados
├── dashboard_trafego.py # Dashboard Streamlit
├── dados_trafego_raw.csv # Dados brutos coletados
├── dados_trafego_tratados.csv # Dados limpos para análise
└── README.md # Documentação do projeto

yaml
Copiar código

---

## ▶️ Como executar o projeto

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/Cezanne369/Trafego_sao_paulo.git
cd Trafego_sao_paulo
2️⃣ Instalar as dependências
bash
Copiar código
pip install -r requirements.txt
3️⃣ Inserir sua API Key TomTom
Abra coleta_trafego_sp.py e adicione sua chave:

python
Copiar código
API = "SUA_TOMTOM_API_KEY"
4️⃣ Rodar a coleta de dados
bash
Copiar código
python coleta_trafego_sp.py
5️⃣ Tratar os dados
bash
Copiar código
python limpeza_trafego.py
6️⃣ Abrir o dashboard
bash
Copiar código
streamlit run dashboard_trafego.py
📌 Exemplo do Dashboard
O painel exibe:

Indicadores de fluidez

Tendência de velocidade ao longo do tempo

Mapa interativo com pontos monitorados

Status de congestionamento em tempo real

🛣️ Pontos de coleta utilizados
Os dados são coletados em locais estratégicos da cidade de São Paulo, como:

Marginal Tietê

Marginal Pinheiros

Avenida Paulista

23 de Maio

Radial Leste
(a lista pode ser expandida facilmente)

🏗️ Melhorias futuras
Persistência dos dados em banco de dados (PostgreSQL / BigQuery)

ML para prever congestionamento

Notificações automáticas (Telegram / E-mail)

API própria para os dados históricos coletados

👨‍💻 Autor Jean
Projeto desenvolvido para aprimorar habilidades em:

Data Engineering
APIs
ETL
Visualização de Dados
Python para automação

