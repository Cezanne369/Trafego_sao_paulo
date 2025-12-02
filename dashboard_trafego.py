# dashboard_trafego.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import folium
from streamlit_folium import st_folium
import branca.colormap as cm

st.set_page_config(page_title="Dashboard Tráfego SP", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def load_data(path="dados_trafego_tratados.csv"):
    df = pd.read_csv(path)
    # garantir tipos corretos
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    else:
        # tentar outras possíveis colunas
        df["timestamp"] = pd.to_datetime(df.iloc[:,0], errors='coerce')
    # colunas esperadas: local, lat, lon, velocidade_atual, velocidade_livre, congestao, hora, dia_semana, periodo
    # preencher lat/lon se faltarem
    if "lat" not in df.columns or "lon" not in df.columns:
        df["lat"] = np.nan
        df["lon"] = np.nan
    return df

df = load_data()

# --- Sidebar filters
st.sidebar.header("Filtros")
locals_available = df["local"].unique().tolist()
selected_locals = st.sidebar.multiselect("Locais", options=locals_available, default=locals_available)
periods = ["manha", "tarde", "noite", "madrugada"]
selected_periods = st.sidebar.multiselect("Períodos", options=periods, default=periods)
days = list(range(0,7))
selected_days = st.sidebar.multiselect("Dias da semana (0=Seg)", options=days, default=days)
date_min = df["timestamp"].min()
date_max = df["timestamp"].max()
start_date, end_date = st.sidebar.date_input("Intervalo de datas", value=[date_min.date(), date_max.date()])

# Apply filters
mask = df["local"].isin(selected_locals) & df["periodo"].isin(selected_periods) & df["dia_semana"].isin(selected_days)
mask &= (df["timestamp"].dt.date >= start_date) & (df["timestamp"].dt.date <= end_date)
df_f = df[mask].copy()

# Top KPIs
st.title("📊 Dashboard — Previsão & Monitoramento de Tráfego (SP)")
st.write("Visualização exploratória do dataset de tráfego. Dados em tempo real coletados por pontos da cidade.")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("Registros", f"{len(df_f):,}")
with kpi2:
    st.metric("Locais selecionados", len(df_f["local"].unique()))
with kpi3:
    avg_cong = round(df_f["congestao"].mean() if not df_f.empty else 0, 2)
    st.metric("Congestão média (%)", f"{avg_cong}%")
with kpi4:
    avg_vel = round(df_f["velocidade_atual"].mean() if not df_f.empty else 0, 2)
    st.metric("Velocidade média (km/h)", f"{avg_vel} km/h")

st.markdown("---")

# Layout dos gráficos
left_col, right_col = st.columns((2,1))

# --- Left column: time series + bar + boxplot
with left_col:
    st.subheader("Série temporal — Congestionamento")
    if df_f.empty:
        st.info("Sem dados para o filtro selecionado.")
    else:
        # agregação temporal (resample por minuto)
        temp = df_f.set_index("timestamp").groupby("local")["congestao"]
        # plotly line por local (média móvel de 3 pontos para suavizar)
        fig_ts = px.line(df_f, x="timestamp", y="congestao", color="local",
                         title="Congestionamento ao longo do tempo",
                         labels={"congestao": "Congestão (%)", "timestamp": "Data/Hora"})
        fig_ts.update_layout(height=400, legend_title_text="Local")
        st.plotly_chart(fig_ts, use_container_width=True)

    st.subheader("Congestão média por local")
    if not df_f.empty:
        mean_by_local = df_f.groupby("local")["congestao"].mean().reset_index().sort_values("congestao", ascending=False)
        fig_bar = px.bar(mean_by_local, x="local", y="congestao", color="congestao",
                         color_continuous_scale="OrRd", labels={"congestao":"Congestão (%)","local":"Local"},
                         title="Congestão média por local")
        fig_bar.update_layout(height=350)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Variação do congestionamento por período (Boxplot)")
    if not df_f.empty:
        fig_box = px.box(df_f, x="periodo", y="congestao", color="periodo",
                         title="Distribuição do congestionamento por período do dia",
                         labels={"congestao":"Congestão (%)","periodo":"Período"})
        fig_box.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

# --- Right column: Heatmap + mapa
with right_col:
    st.subheader("Heatmap: dia da semana × hora")
    if df_f.empty:
        st.write("Sem dados para gerar heatmap.")
    else:
        pivot = df_f.pivot_table(values="congestao", index="dia_semana", columns="hora", aggfunc="mean")
        # garantir ordenação de 0 a 23 nas colunas
        pivot = pivot.reindex(columns=range(0,24), fill_value=np.nan)
        fig_heat = px.imshow(pivot, labels=dict(x="Hora", y="Dia da semana", color="Congestão (%)"),
                             x=pivot.columns, y=["Seg","Ter","Qua","Qui","Sex","Sab","Dom"][:pivot.shape[0]],
                             title="Heatmap de congestão (dia da semana × hora)")
        fig_heat.update_layout(height=450)
        st.plotly_chart(fig_heat, use_container_width=True)

    st.subheader("Mapa interativo (Folium)")
    # mapa centrado na média das coordenadas disponíveis
    coords = df_f[["lat","lon"]].dropna()
    if coords.empty:
        st.info("Não há coordenadas disponíveis para desenhar o mapa.")
    else:
        map_center = [coords["lat"].mean(), coords["lon"].mean()]
        m = folium.Map(location=map_center, zoom_start=12, tiles="OpenStreetMap")
        # colormap
        colormap = cm.LinearColormap(["green","yellow","orange","red"], vmin=0, vmax=100, caption="Congestão (%)")
        colormap.add_to(m)
        # agregar por local a média de congestão e coordenadas médias
        agg = df_f.groupby("local").agg({
            "congestao": "mean",
            "lat": "mean",
            "lon": "mean",
            "velocidade_atual": "mean"
        }).reset_index()
        for _, row in agg.iterrows():
            congestion = float(row["congestao"])
            folium.CircleMarker(
                location=[row["lat"], row["lon"]],
                radius=12,
                color=colormap(congestion),
                fill=True,
                fill_color=colormap(congestion),
                fill_opacity=0.8,
                popup=folium.Popup(f"<b>{row['local']}</b><br>Congestão média: {congestion:.2f}%<br>Vel média: {row['velocidade_atual']:.1f} km/h", max_width=300)
            ).add_to(m)
        # renderiza no Streamlit
        st_folium(m, width="100%", height=450)

st.markdown("---")
st.caption("Dashboard gerado localmente. Dados: dados_trafego_tratados.csv")
