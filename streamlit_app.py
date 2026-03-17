import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from io import BytesIO
import base64

# ============================================
# CONFIGURACIÓN
# ============================================
st.set_page_config(
    page_title="Yuku Savi | Dashboard",
    page_icon="🌵",
    layout="wide",
    initial_sidebar_state="expanded"
)

SHEET_ID = "169pU5z_xFWBACaXBkTogQzgV15L9cxJZ9kZXvr7dXG8"
STATUS_VENTAS = ['Entregado', 'Pagado', 'Apartado']
STATUS_COTIZACIONES = ['Cotizado']
META_MENSUAL = 300000

# Paleta Power BI
C = {
    'bg': '#1b1d21',
    'bg2': '#252830',
    'card': '#2d313a',
    'card2': '#343942',
    'text': '#ffffff',
    'text2': '#a0aec0',
    'text3': '#718096',
    'accent': '#00d4aa',
    'green': '#00d4aa',
    'red': '#ff6b6b',
    'amber': '#ffc107',
    'blue': '#4dabf7',
    'purple': '#9775fa',
    'border': '#3d4350',
}

# ============================================
# CSS POWER BI ULTRA
# ============================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {{
    --bg: {C['bg']};
    --bg2: {C['bg2']};
    --card: {C['card']};
    --card2: {C['card2']};
    --text: {C['text']};
    --text2: {C['text2']};
    --text3: {C['text3']};
    --accent: {C['accent']};
    --green: {C['green']};
    --red: {C['red']};
    --amber: {C['amber']};
    --blue: {C['blue']};
    --purple: {C['purple']};
    --border: {C['border']};
}}

html, body, [class*="css"] {{
    font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif !important;
}}

.stApp {{
    background: var(--bg) !important;
}}

#MainMenu, footer, header[data-testid="stHeader"], .stDeployButton {{
    display: none !important;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}}

section[data-testid="stSidebar"] > div:first-child {{
    background: var(--bg2) !important;
    padding-top: 0 !important;
}}

/* Tabs Power BI Style */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0;
    background: var(--bg2);
    border-radius: 4px;
    padding: 4px;
    border: 1px solid var(--border);
}}

.stTabs [data-baseweb="tab"] {{
    background: transparent;
    border: none;
    color: var(--text3);
    font-size: 13px;
    font-weight: 500;
    padding: 10px 20px;
    border-radius: 4px;
    transition: all 0.2s ease;
}}

.stTabs [data-baseweb="tab"]:hover {{
    background: var(--card);
    color: var(--text);
}}

.stTabs [aria-selected="true"] {{
    background: var(--accent) !important;
    color: #000 !important;
    font-weight: 600 !important;
}}

.stTabs [data-baseweb="tab-panel"] {{
    padding-top: 20px;
}}

/* Selectbox & Text Input */
.stSelectbox > div > div, .stTextInput > div > div {{
    background: var(--card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--text) !important;
}}

.stSelectbox > div > div:hover, .stTextInput > div > div:focus-within {{
    border-color: var(--accent) !important;
}}

.stSelectbox label, .stTextInput label {{
    color: var(--text3) !important;
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    font-weight: 600 !important;
}}

/* Buttons */
.stButton > button {{
    background: var(--accent) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 4px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 12px 20px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}}

.stButton > button:hover {{
    background: #00b894 !important;
    transform: translateY(-1px) !important;
}}

.stDownloadButton > button {{
    background: var(--card2) !important;
    color: var(--accent) !important;
    border: 1px solid var(--accent) !important;
    border-radius: 4px !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease !important;
}}

.stDownloadButton > button:hover {{
    background: var(--accent) !important;
    color: #000 !important;
}}

/* Cards with animation */
.card {{
    background: var(--card);
    border-radius: 4px;
    padding: 20px;
    border: 1px solid var(--border);
    margin-bottom: 12px;
    transition: all 0.2s ease;
}}

.card:hover {{
    border-color: rgba(0,212,170,0.3);
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}}

.card-title {{
    font-size: 12px;
    color: var(--text2);
    font-weight: 600;
    margin-bottom: 16px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* KPI Cards with pulse animation for highlights */
.kpi-card {{
    background: var(--card);
    border-radius: 4px;
    padding: 18px;
    border: 1px solid var(--border);
    transition: all 0.2s ease;
}}

.kpi-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}}

.kpi-card.accent {{
    background: linear-gradient(135deg, rgba(0,212,170,0.12), var(--card));
    border-color: rgba(0,212,170,0.4);
}}

.kpi-label {{
    font-size: 11px;
    color: var(--text3);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
    margin-bottom: 10px;
}}

.kpi-value {{
    font-size: 26px;
    font-weight: 700;
    color: var(--text);
    line-height: 1.1;
}}

.kpi-value.large {{ font-size: 30px; }}
.kpi-value.accent {{ color: var(--accent); }}

.kpi-delta {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    margin-top: 10px;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
}}

.kpi-delta.up {{
    background: rgba(0,212,170,0.15);
    color: var(--green);
}}

.kpi-delta.down {{
    background: rgba(255,107,107,0.15);
    color: var(--red);
}}

.kpi-delta.neutral {{
    background: rgba(255,193,7,0.15);
    color: var(--amber);
}}

.kpi-sublabel {{
    font-size: 11px;
    color: var(--text3);
    margin-left: 6px;
}}

/* Data Tables with sorting indicators */
.data-table {{
    width: 100%;
    border-collapse: collapse;
}}

.data-table th {{
    text-align: left;
    padding: 12px 10px;
    border-bottom: 1px solid var(--border);
    color: var(--text3);
    font-weight: 600;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    position: sticky;
    top: 0;
    background: var(--card);
    cursor: pointer;
    user-select: none;
    transition: color 0.2s;
}}

.data-table th:hover {{
    color: var(--accent);
}}

.data-table th.center {{ text-align: center; }}
.data-table th.right {{ text-align: right; }}

.data-table td {{
    padding: 14px 10px;
    border-bottom: 1px solid rgba(61,67,80,0.25);
    color: var(--text);
    font-size: 13px;
}}

.data-table td.center {{ text-align: center; }}
.data-table td.right {{ text-align: right; }}
.data-table td.accent {{ color: var(--accent); font-weight: 600; }}

.data-table tr {{
    transition: background 0.15s;
}}

.data-table tr:hover {{
    background: rgba(0,212,170,0.08);
}}

/* Status Badges */
.status-badge {{
    display: inline-flex;
    align-items: center;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
}}

.status-badge.entregado {{ background: rgba(0,212,170,0.15); color: var(--green); }}
.status-badge.pagado {{ background: rgba(77,171,247,0.15); color: var(--blue); }}
.status-badge.apartado {{ background: rgba(151,117,250,0.15); color: var(--purple); }}
.status-badge.cotizado {{ background: rgba(255,193,7,0.15); color: var(--amber); }}

/* Funnel */
.funnel-item {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 18px;
    border-radius: 4px;
    color: white;
    font-weight: 500;
    font-size: 13px;
    margin-bottom: 8px;
    transition: transform 0.2s;
}}

.funnel-item:hover {{
    transform: scale(1.02);
}}

.funnel-count {{
    background: rgba(0,0,0,0.25);
    padding: 4px 12px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 14px;
}}

/* Inventory */
.inv-item {{ margin-bottom: 16px; }}
.inv-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
.inv-name {{ font-size: 13px; color: var(--text); }}
.inv-stock {{ font-size: 14px; font-weight: 600; }}
.inv-badge {{ width: 22px; height: 22px; border-radius: 4px; display: inline-flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; margin-left: 8px; }}
.inv-badge.ok {{ background: rgba(0,212,170,0.15); color: var(--green); }}
.inv-badge.warning {{ background: rgba(255,193,7,0.15); color: var(--amber); }}
.inv-badge.danger {{ background: rgba(255,107,107,0.15); color: var(--red); }}
.progress-bar {{ height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; }}
.progress-fill {{ height: 100%; border-radius: 3px; transition: width 0.5s ease; }}

/* Inventory Cards Grid */
.inv-card {{
    background: var(--card);
    border-radius: 4px;
    padding: 16px;
    border: 1px solid var(--border);
    text-align: center;
    transition: all 0.2s;
}}

.inv-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}}

.inv-card-title {{ font-size: 13px; color: var(--text); font-weight: 600; margin-bottom: 8px; }}
.inv-card-stock {{ font-size: 32px; font-weight: 700; margin-bottom: 8px; }}
.inv-card-label {{ font-size: 10px; color: var(--text3); text-transform: uppercase; }}

/* Donut Legend */
.donut-legend {{ margin-top: 12px; }}
.donut-legend-item {{ display: flex; align-items: center; gap: 10px; margin-bottom: 8px; font-size: 12px; }}
.donut-legend-dot {{ width: 12px; height: 12px; border-radius: 3px; flex-shrink: 0; }}
.donut-legend-name {{ flex: 1; color: var(--text2); }}
.donut-legend-value {{ color: var(--text); font-weight: 600; }}

/* Header */
.main-header {{ display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; margin-bottom: 20px; border-bottom: 1px solid var(--border); }}
.main-title {{ font-size: 22px; font-weight: 600; color: var(--text); margin: 0; }}
.main-subtitle {{ font-size: 13px; color: var(--text3); margin-top: 4px; }}

/* Sidebar */
.sidebar-logo {{ text-align: center; padding: 24px 16px; background: var(--card); border-radius: 4px; margin-bottom: 20px; border: 1px solid rgba(0,212,170,0.25); }}
.sidebar-icon {{ font-size: 36px; margin-bottom: 8px; }}
.sidebar-title {{ color: var(--accent); font-size: 16px; font-weight: 700; letter-spacing: 3px; }}
.sidebar-subtitle {{ color: var(--text3); font-size: 9px; letter-spacing: 2px; margin-top: 4px; }}
.sidebar-section {{ font-size: 10px; color: var(--text3); text-transform: uppercase; letter-spacing: 1px; font-weight: 700; margin: 20px 0 12px; display: flex; align-items: center; gap: 6px; }}
.sidebar-footer {{ text-align: center; padding-top: 20px; margin-top: 24px; border-top: 1px solid var(--border); }}
.sidebar-footer-brand {{ color: var(--accent); font-weight: 600; font-size: 13px; }}

/* Footer */
.main-footer {{ text-align: center; padding: 24px; margin-top: 32px; border-top: 1px solid var(--border); color: var(--text3); font-size: 12px; }}

/* Table container with search */
.table-container {{ max-height: 500px; overflow-y: auto; border-radius: 4px; }}

/* Stats row */
.stats-row {{ display: flex; gap: 16px; margin-bottom: 20px; flex-wrap: wrap; }}
.stat-chip {{ background: var(--card); border: 1px solid var(--border); border-radius: 4px; padding: 12px 20px; display: flex; align-items: center; gap: 10px; transition: all 0.2s; }}
.stat-chip:hover {{ border-color: var(--accent); }}
.stat-chip-value {{ font-size: 18px; font-weight: 700; color: var(--accent); }}
.stat-chip-label {{ font-size: 11px; color: var(--text3); text-transform: uppercase; }}

/* Export buttons row */
.export-row {{ display: flex; gap: 10px; margin-bottom: 16px; }}

/* Search highlight */
.search-highlight {{ background: rgba(0,212,170,0.3); padding: 2px 4px; border-radius: 2px; }}

[data-testid="column"] {{ padding: 0 6px !important; }}
.js-plotly-plot .plotly .main-svg {{ background: transparent !important; }}

/* Animations */
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.animate-in {{
    animation: fadeIn 0.3s ease-out;
}}
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNCIONES DE DATOS
# ============================================
def find_col(df, names):
    for n in names:
        if n in df.columns: return n
        for c in df.columns:
            if c.lower().strip() == n.lower().strip(): return c
    return None

def clean_money(v):
    if pd.isna(v): return 0.0
    if isinstance(v, (int, float)): return float(v)
    try: return float(str(v).replace('$','').replace(',','').strip())
    except: return 0.0

@st.cache_data(ttl=120)
def load_sheet(name):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={name}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

def load_all():
    return load_sheet("VENTAS"), load_sheet("INVENTARIO"), load_sheet("GASTOS")

def process_ventas(df):
    if df.empty: return df
    df = df.copy()
    for c in ['Precio Unitario', 'Subtotal', 'Total', 'Costo Envío']:
        if c in df.columns: df[c] = df[c].apply(clean_money)
    if 'Cantidad' in df.columns:
        df['Cantidad'] = pd.to_numeric(df['Cantidad'], errors='coerce').fillna(0).astype(int)
    fc = find_col(df, ['Fecha'])
    if fc: df[fc] = pd.to_datetime(df[fc], errors='coerce')
    return df

def process_inventario(df):
    if df.empty: return df
    df = df.copy()
    for c in ['Stock Actual', 'Stock Mínimo', 'Stock Máximo', 'Precio Venta', 'Costo Producción']:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
    return df

def process_gastos(df):
    if df.empty: return df
    df = df.copy()
    mc = find_col(df, ['Monto'])
    if mc: df[mc] = df[mc].apply(clean_money)
    return df

def filter_periodo(df, periodo, fecha_col):
    if df.empty or not fecha_col or periodo == "Todos": return df
    df = df.copy()
    df[fecha_col] = pd.to_datetime(df[fecha_col], errors='coerce')
    today = datetime.now()
    
    if periodo == "Hoy":
        mask = df[fecha_col].dt.date == today.date()
    elif periodo == "Esta semana":
        start = today - timedelta(days=today.weekday())
        mask = df[fecha_col].dt.date >= start.date()
    elif periodo == "Este mes":
        mask = (df[fecha_col].dt.month == today.month) & (df[fecha_col].dt.year == today.year)
    elif periodo == "Trimestre":
        q = (today.month - 1) // 3
        start_m = q * 3 + 1
        mask = (df[fecha_col].dt.month >= start_m) & (df[fecha_col].dt.month < start_m + 3) & (df[fecha_col].dt.year == today.year)
    elif periodo == "Año":
        mask = df[fecha_col].dt.year == today.year
    else:
        return df
    return df[mask]

def get_previous_period_data(df, fecha_col, periodo):
    """Obtiene datos del periodo anterior para calcular deltas reales"""
    if df.empty or not fecha_col: return pd.DataFrame()
    df = df.copy()
    df[fecha_col] = pd.to_datetime(df[fecha_col], errors='coerce')
    today = datetime.now()
    
    if periodo == "Este mes":
        prev_month = today.month - 1 if today.month > 1 else 12
        prev_year = today.year if today.month > 1 else today.year - 1
        mask = (df[fecha_col].dt.month == prev_month) & (df[fecha_col].dt.year == prev_year)
    elif periodo == "Esta semana":
        start = today - timedelta(days=today.weekday() + 7)
        end = today - timedelta(days=today.weekday() + 1)
        mask = (df[fecha_col].dt.date >= start.date()) & (df[fecha_col].dt.date <= end.date())
    elif periodo == "Trimestre":
        q = (today.month - 1) // 3
        prev_q = q - 1 if q > 0 else 3
        prev_year = today.year if q > 0 else today.year - 1
        start_m = prev_q * 3 + 1
        mask = (df[fecha_col].dt.month >= start_m) & (df[fecha_col].dt.month < start_m + 3) & (df[fecha_col].dt.year == prev_year)
    elif periodo == "Año":
        mask = df[fecha_col].dt.year == today.year - 1
    else:
        return pd.DataFrame()
    return df[mask]

def calc_delta(current, previous):
    """Calcula el porcentaje de cambio"""
    if previous == 0: return 100.0 if current > 0 else 0.0
    return ((current - previous) / previous) * 100

def search_dataframe(df, query, columns):
    """Búsqueda en dataframe"""
    if not query or df.empty: return df
    query = query.lower()
    mask = pd.Series([False] * len(df))
    for col in columns:
        if col in df.columns:
            mask |= df[col].astype(str).str.lower().str.contains(query, na=False)
    return df[mask]

def sort_dataframe(df, sort_col, ascending=True):
    """Ordena dataframe por columna"""
    if sort_col and sort_col in df.columns:
        return df.sort_values(by=sort_col, ascending=ascending)
    return df

def to_excel(df):
    """Convierte DataFrame a Excel/CSV para descarga"""
    output = BytesIO()
    try:
        # Intentar xlsxwriter primero (más común en Streamlit Cloud)
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Datos')
        return output.getvalue(), 'xlsx'
    except:
        # Fallback a CSV si no hay engine disponible
        return df.to_csv(index=False).encode('utf-8'), 'csv'

# ============================================
# GRÁFICOS PLOTLY
# ============================================
def chart_bars_meta(df, fecha_col, total_col, meta):
    if df.empty or not fecha_col or not total_col: return None
    
    df_temp = df.copy()
    df_temp['_fecha'] = pd.to_datetime(df_temp[fecha_col], errors='coerce')
    df_temp['_total'] = pd.to_numeric(df_temp[total_col], errors='coerce').fillna(0)
    
    monthly = df_temp.groupby(df_temp['_fecha'].dt.to_period('M')).agg({'_total': 'sum'}).reset_index()
    monthly['mes_label'] = monthly['_fecha'].dt.strftime('%b')
    
    if monthly.empty: return None
    
    colors = [C['accent'] if v >= meta else C['amber'] if v >= meta*0.7 else C['red'] for v in monthly['_total']]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly['mes_label'], y=[meta]*len(monthly),
        mode='lines', name='Meta',
        line=dict(color=C['amber'], width=2, dash='dot'),
        hoverinfo='skip'
    ))
    fig.add_trace(go.Bar(
        x=monthly['mes_label'], y=monthly['_total'],
        name='Ventas',
        marker=dict(color=colors),
        hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=C['text3'], family='Inter', size=11),
        margin=dict(l=50, r=20, t=10, b=40),
        height=200,
        showlegend=False,
        yaxis=dict(tickformat='$,.0f', gridcolor=C['border'], gridwidth=0.5, zeroline=False, tickfont=dict(size=10)),
        xaxis=dict(gridcolor='rgba(0,0,0,0)', tickfont=dict(size=10)),
        bargap=0.4,
        hovermode='x unified'
    )
    return fig

def chart_gauge(value, max_val):
    pct = min((value / max_val) * 100, 100) if max_val > 0 else 0
    color = C['green'] if pct >= 80 else C['amber'] if pct >= 50 else C['red']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct,
        number={'suffix': '%', 'font': {'size': 40, 'color': C['text'], 'family': 'Inter'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 0, 'tickcolor': 'rgba(0,0,0,0)', 'tickfont': {'size': 1, 'color': 'rgba(0,0,0,0)'}},
            'bar': {'color': color, 'thickness': 0.8},
            'bgcolor': C['border'],
            'borderwidth': 0,
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=180,
        margin=dict(l=20, r=20, t=40, b=10),
        font=dict(family='Inter')
    )
    return fig

def chart_donut(labels, values, center_text):
    colors_list = [C['accent'], C['blue'], C['purple'], C['amber'], C['red']]
    
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.65,
        marker=dict(colors=colors_list[:len(labels)], line=dict(color=C['bg'], width=2)),
        textinfo='percent',
        textposition='outside',
        textfont=dict(color=C['text'], size=11, family='Inter'),
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>',
        direction='clockwise',
        sort=False
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=C['text3'], family='Inter'),
        margin=dict(l=10, r=10, t=10, b=10),
        height=180,
        showlegend=False,
        annotations=[dict(text=f"<b>{center_text}</b>", x=0.5, y=0.5, font=dict(size=16, color=C['accent'], family='Inter'), showarrow=False)]
    )
    return fig

def chart_sparkline(values):
    fig = go.Figure(go.Scatter(
        y=values, mode='lines+markers',
        line=dict(color=C['accent'], width=2),
        marker=dict(size=4, color=C['accent']),
        hoverinfo='skip',
        fill='tozeroy',
        fillcolor='rgba(0,212,170,0.1)'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=5, b=5),
        height=50,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False
    )
    return fig

def chart_treemap(df, prod_col, value_col):
    """Treemap de productos"""
    if df.empty or not prod_col or not value_col: return None
    
    data = df.groupby(prod_col)[value_col].sum().reset_index()
    data.columns = ['Producto', 'Valor']
    
    fig = px.treemap(
        data, path=['Producto'], values='Valor',
        color='Valor',
        color_continuous_scale=[[0, C['card2']], [0.5, C['blue']], [1, C['accent']]]
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=C['text'], family='Inter', size=12),
        margin=dict(l=0, r=0, t=0, b=0),
        height=250,
        coloraxis_showscale=False
    )
    fig.update_traces(
        textfont=dict(size=14, color='white'),
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<extra></extra>'
    )
    return fig

def chart_heatmap(df, fecha_col, total_col):
    """Heatmap de ventas por día de semana y hora/semana"""
    if df.empty or not fecha_col or not total_col: return None
    
    df_temp = df.copy()
    df_temp['_fecha'] = pd.to_datetime(df_temp[fecha_col], errors='coerce')
    df_temp['_total'] = pd.to_numeric(df_temp[total_col], errors='coerce').fillna(0)
    df_temp['dia_semana'] = df_temp['_fecha'].dt.dayofweek
    df_temp['semana'] = df_temp['_fecha'].dt.isocalendar().week
    
    pivot = df_temp.groupby(['dia_semana', 'semana'])['_total'].sum().reset_index()
    pivot_table = pivot.pivot(index='dia_semana', columns='semana', values='_total').fillna(0)
    
    dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    
    fig = go.Figure(go.Heatmap(
        z=pivot_table.values,
        x=[f'S{int(c)}' for c in pivot_table.columns],
        y=[dias[i] for i in pivot_table.index],
        colorscale=[[0, C['bg2']], [0.5, C['blue']], [1, C['accent']]],
        hovertemplate='%{y}, Semana %{x}<br>$%{z:,.0f}<extra></extra>',
        showscale=False
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=C['text3'], family='Inter', size=11),
        margin=dict(l=50, r=10, t=10, b=30),
        height=200,
        xaxis=dict(tickfont=dict(size=9)),
        yaxis=dict(tickfont=dict(size=10))
    )
    return fig

def chart_area_tendencia(df, fecha_col, total_col):
    """Área apilada de tendencia de ventas"""
    if df.empty or not fecha_col or not total_col: return None
    
    df_temp = df.copy()
    df_temp['_fecha'] = pd.to_datetime(df_temp[fecha_col], errors='coerce')
    df_temp['_total'] = pd.to_numeric(df_temp[total_col], errors='coerce').fillna(0)
    
    daily = df_temp.groupby(df_temp['_fecha'].dt.date).agg({'_total': 'sum'}).reset_index()
    daily.columns = ['fecha', 'ventas']
    daily['acumulado'] = daily['ventas'].cumsum()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily['fecha'], y=daily['acumulado'],
        fill='tozeroy',
        mode='lines',
        line=dict(color=C['accent'], width=2),
        fillcolor='rgba(0,212,170,0.2)',
        name='Acumulado',
        hovertemplate='%{x}<br>Acumulado: $%{y:,.0f}<extra></extra>'
    ))
    fig.add_trace(go.Bar(
        x=daily['fecha'], y=daily['ventas'],
        marker=dict(color=C['blue'], opacity=0.6),
        name='Diario',
        hovertemplate='%{x}<br>Diario: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=C['text3'], family='Inter', size=11),
        margin=dict(l=50, r=20, t=10, b=40),
        height=200,
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=1, font=dict(size=10)),
        yaxis=dict(tickformat='$,.0f', gridcolor=C['border'], gridwidth=0.5, zeroline=False),
        xaxis=dict(gridcolor='rgba(0,0,0,0)'),
        hovermode='x unified',
        barmode='overlay'
    )
    return fig

def chart_gastos_categoria(df, cat_col, monto_col):
    if df.empty or not cat_col or not monto_col: return None
    
    data = df.groupby(cat_col)[monto_col].sum().sort_values(ascending=True).tail(8)
    colors_list = [C['accent'], C['blue'], C['purple'], C['amber'], C['red'], C['green'], '#ff9ff3', '#54a0ff']
    
    fig = go.Figure(go.Bar(
        x=data.values,
        y=data.index,
        orientation='h',
        marker=dict(color=colors_list[:len(data)]),
        hovertemplate='<b>%{y}</b><br>$%{x:,.0f}<extra></extra>'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=C['text3'], family='Inter', size=11),
        margin=dict(l=120, r=20, t=10, b=40),
        height=300,
        xaxis=dict(tickformat='$,.0f', gridcolor=C['border'], gridwidth=0.5, zeroline=False),
        yaxis=dict(gridcolor='rgba(0,0,0,0)'),
        hovermode='y unified'
    )
    return fig

# ============================================
# COMPONENTES HTML
# ============================================
def html_kpi(label, value, prefix="$", suffix="", delta=None, delta_label="vs periodo ant.", accent=False, large=False):
    if prefix == "$":
        fmt_val = f"${value:,.0f}"
    elif suffix == "%":
        fmt_val = f"{value:.1f}%"
    else:
        fmt_val = f"{value:,.0f}"
    
    card_cls = "kpi-card accent" if accent else "kpi-card"
    val_cls = "kpi-value" + (" large" if large else "") + (" accent" if accent else "")
    
    delta_html = ""
    if delta is not None:
        if delta > 0:
            d_cls, arrow = "up", "▲"
        elif delta < 0:
            d_cls, arrow = "down", "▼"
        else:
            d_cls, arrow = "neutral", "●"
        delta_html = f'<div class="kpi-delta {d_cls}">{arrow} {abs(delta):.1f}%<span class="kpi-sublabel">{delta_label}</span></div>'
    
    return f'<div class="{card_cls}"><div class="kpi-label">{label}</div><div class="{val_cls}">{fmt_val}</div>{delta_html}</div>'

def html_table_ventas(df, fecha_col, total_col, cant_col, status_col, search_query=""):
    if df.empty: return '<p style="color: var(--text3);">Sin datos</p>'
    
    rows = ""
    for _, row in df.iterrows():
        folio = str(row.get('Folio', '-'))
        fecha = pd.to_datetime(row.get(fecha_col), errors='coerce')
        fecha_str = fecha.strftime('%d/%m/%Y') if pd.notna(fecha) else '-'
        cliente = str(row.get('Cliente', '-'))
        producto = str(row.get('Producto', '-'))
        cant = int(row.get(cant_col, 0)) if cant_col else 0
        total = row.get(total_col, 0) if total_col else 0
        canal = str(row.get('Canal', '-'))
        status = row.get(status_col, '-') if status_col else '-'
        
        # Highlight search matches
        if search_query:
            sq = search_query.lower()
            if sq in folio.lower(): folio = folio.replace(folio, f'<span class="search-highlight">{folio}</span>')
            if sq in cliente.lower(): cliente = f'<span class="search-highlight">{cliente}</span>'
            if sq in producto.lower(): producto = f'<span class="search-highlight">{producto}</span>'
        
        status_cls = status.lower().replace(' ', '') if isinstance(status, str) else ''
        
        rows += f'''<tr>
            <td>{folio}</td>
            <td>{fecha_str}</td>
            <td>{cliente}</td>
            <td>{producto}</td>
            <td class="center">{cant}</td>
            <td class="right accent">${total:,.0f}</td>
            <td class="center">{canal}</td>
            <td class="center"><span class="status-badge {status_cls}">{status}</span></td>
        </tr>'''
    
    return f'''<div class="table-container">
        <table class="data-table">
            <thead>
                <tr>
                    <th>Folio ↕</th>
                    <th>Fecha ↕</th>
                    <th>Cliente ↕</th>
                    <th>Producto ↕</th>
                    <th class="center">Cant.</th>
                    <th class="right">Total ↕</th>
                    <th class="center">Canal</th>
                    <th class="center">Status</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    </div>'''

def html_table_productos(data, columns):
    if not data: return '<p style="color: var(--text3);">Sin datos</p>'
    
    headers = "".join([f'<th class="{c.get("align","")}">{c["label"]}</th>' for c in columns])
    rows = ""
    for row in data:
        cells = ""
        for col in columns:
            v = row.get(col['key'], '')
            if col.get('prefix') == '$' and isinstance(v, (int, float)):
                fmt = f"${v:,.0f}"
            elif col.get('suffix') == '%' and isinstance(v, (int, float)):
                fmt = f"{v}%"
            else:
                fmt = str(v)
            cls = col.get('align', '')
            if col.get('highlight'): cls += ' accent'
            cells += f'<td class="{cls}">{fmt}</td>'
        rows += f'<tr>{cells}</tr>'
    
    return f'<table class="data-table"><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table>'

def html_funnel(data):
    colors = [C['blue'], C['purple'], C['amber'], C['green']]
    widths = [100, 85, 70, 55]
    html = ""
    for i, item in enumerate(data):
        color = colors[i % len(colors)]
        width = widths[i] if i < len(widths) else 50
        html += f'<div class="funnel-item" style="width:{width}%; background:linear-gradient(90deg,{color}dd,{color}88); margin:0 auto;"><span>{item["etapa"]}</span><span class="funnel-count">{item["count"]}</span></div>'
    return html

def html_inventory(data):
    html = ""
    for item in data:
        stock, minimo = item['stock'], item['minimo']
        if stock <= minimo * 0.5:
            status, color, badge = 'danger', C['red'], '⚠'
        elif stock <= minimo:
            status, color, badge = 'warning', C['amber'], '!'
        else:
            status, color, badge = 'ok', C['green'], '✓'
        pct = min((stock / (minimo * 3)) * 100, 100) if minimo > 0 else 0
        html += f'''<div class="inv-item">
            <div class="inv-header">
                <span class="inv-name">{item['producto']}</span>
                <div><span class="inv-stock" style="color:{color};">{int(stock)}</span><span class="inv-badge {status}">{badge}</span></div>
            </div>
            <div class="progress-bar"><div class="progress-fill" style="width:{pct}%; background:{color};"></div></div>
        </div>'''
    return html

def html_inventory_cards(df, prod_col, stock_col, min_col):
    if df.empty: return ''
    html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px;">'
    for _, row in df.iterrows():
        prod = row[prod_col]
        stock = int(row[stock_col]) if stock_col else 0
        minimo = int(row[min_col]) if min_col else 10
        
        if stock <= minimo * 0.5:
            color = C['red']
        elif stock <= minimo:
            color = C['amber']
        else:
            color = C['green']
        
        html += f'''<div class="inv-card">
            <div class="inv-card-title">{prod}</div>
            <div class="inv-card-stock" style="color: {color};">{stock}</div>
            <div class="inv-card-label">En stock (mín: {minimo})</div>
        </div>'''
    html += '</div>'
    return html

def html_legend(items, colors_list):
    html = '<div class="donut-legend">'
    for i, item in enumerate(items):
        color = colors_list[i % len(colors_list)]
        html += f'<div class="donut-legend-item"><div class="donut-legend-dot" style="background:{color};"></div><span class="donut-legend-name">{item["name"]}</span><span class="donut-legend-value">{item["pct"]:.0f}%</span></div>'
    html += '</div>'
    return html

def html_table_gastos(df, fecha_col, cat_col, monto_col, search_query=""):
    if df.empty: return '<p style="color: var(--text3);">Sin datos</p>'
    
    rows = ""
    for _, row in df.iterrows():
        fecha = pd.to_datetime(row.get(fecha_col), errors='coerce')
        fecha_str = fecha.strftime('%d/%m/%Y') if pd.notna(fecha) else '-'
        categoria = str(row.get(cat_col, '-'))
        concepto = str(row.get('Concepto', row.get('Descripción', '-')))
        monto = row.get(monto_col, 0)
        proveedor = str(row.get('Proveedor', '-'))
        
        if search_query:
            sq = search_query.lower()
            if sq in categoria.lower(): categoria = f'<span class="search-highlight">{categoria}</span>'
            if sq in concepto.lower(): concepto = f'<span class="search-highlight">{concepto}</span>'
            if sq in proveedor.lower(): proveedor = f'<span class="search-highlight">{proveedor}</span>'
        
        rows += f'''<tr>
            <td>{fecha_str}</td>
            <td>{categoria}</td>
            <td>{concepto}</td>
            <td class="right accent">${monto:,.0f}</td>
            <td>{proveedor}</td>
        </tr>'''
    
    return f'''<div class="table-container">
        <table class="data-table">
            <thead>
                <tr>
                    <th>Fecha ↕</th>
                    <th>Categoría ↕</th>
                    <th>Concepto</th>
                    <th class="right">Monto ↕</th>
                    <th>Proveedor</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    </div>'''

# ============================================
# MAIN APP
# ============================================
def main():
    ventas_raw, inventario_raw, gastos_raw = load_all()
    ventas = process_ventas(ventas_raw)
    inventario = process_inventario(inventario_raw)
    gastos = process_gastos(gastos_raw)
    
    if ventas.empty:
        st.error("⚠️ No se pudieron cargar los datos")
        st.stop()
    
    # ========== SIDEBAR ==========
    with st.sidebar:
        st.markdown('''<div class="sidebar-logo">
            <div class="sidebar-icon">🌵</div>
            <div class="sidebar-title">YUKU SAVI</div>
            <div class="sidebar-subtitle">MEZCAL ARTESANAL</div>
        </div>''', unsafe_allow_html=True)
        
        if st.button("↻ Actualizar", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown('<div class="sidebar-section">⚙️ FILTROS</div>', unsafe_allow_html=True)
        
        periodo = st.selectbox("Periodo", ["Todos", "Hoy", "Esta semana", "Este mes", "Trimestre", "Año"], index=3)
        canales = ["Todos"] + sorted(ventas['Canal'].dropna().unique().tolist()) if 'Canal' in ventas.columns else ["Todos"]
        canal = st.selectbox("Canal", canales)
        vendedores = ["Todos"] + sorted(ventas['Vendedor'].dropna().unique().tolist()) if 'Vendedor' in ventas.columns else ["Todos"]
        vendedor = st.selectbox("Vendedor", vendedores)
        productos = ["Todos"] + sorted(ventas['Producto'].dropna().unique().tolist()) if 'Producto' in ventas.columns else ["Todos"]
        producto = st.selectbox("Producto", productos)
        
        # Filtrar periodo actual
        df = ventas.copy()
        fecha_col = find_col(df, ['Fecha'])
        df = filter_periodo(df, periodo, fecha_col)
        if canal != "Todos" and 'Canal' in df.columns: df = df[df['Canal'] == canal]
        if vendedor != "Todos" and 'Vendedor' in df.columns: df = df[df['Vendedor'] == vendedor]
        if producto != "Todos" and 'Producto' in df.columns: df = df[df['Producto'] == producto]
        
        # Filtrar periodo anterior para deltas
        df_prev = ventas.copy()
        df_prev = get_previous_period_data(df_prev, fecha_col, periodo)
        if canal != "Todos" and 'Canal' in df_prev.columns: df_prev = df_prev[df_prev['Canal'] == canal]
        if vendedor != "Todos" and 'Vendedor' in df_prev.columns: df_prev = df_prev[df_prev['Vendedor'] == vendedor]
        if producto != "Todos" and 'Producto' in df_prev.columns: df_prev = df_prev[df_prev['Producto'] == producto]
        
        status_col = find_col(df, ['Status'])
        df_ventas = df[df[status_col].isin(STATUS_VENTAS)] if status_col else df
        df_cotiz = df[df[status_col].isin(STATUS_COTIZACIONES)] if status_col else pd.DataFrame()
        df_ventas_prev = df_prev[df_prev[status_col].isin(STATUS_VENTAS)] if status_col and not df_prev.empty else pd.DataFrame()
        
        st.markdown('<div class="sidebar-section">📈 TENDENCIA</div>', unsafe_allow_html=True)
        total_col = find_col(df_ventas, ['Total'])
        if fecha_col and total_col and not df_ventas.empty:
            df_ventas_copy = df_ventas.copy()
            df_ventas_copy[fecha_col] = pd.to_datetime(df_ventas_copy[fecha_col], errors='coerce')
            daily = df_ventas_copy.groupby(df_ventas_copy[fecha_col].dt.date)[total_col].sum().tail(7)
            if len(daily) > 1:
                st.plotly_chart(chart_sparkline(daily.values.tolist()), use_container_width=True, config={'displayModeBar': False})
        
        st.markdown('''<div class="sidebar-footer">
            <div style="font-size:9px; color:var(--text3);">Powered by</div>
            <div class="sidebar-footer-brand">SINAPSIS</div>
        </div>''', unsafe_allow_html=True)
    
    # ========== CALCULAR MÉTRICAS CON DELTAS REALES ==========
    total_col = find_col(df_ventas, ['Total'])
    cant_col = find_col(df_ventas, ['Cantidad'])
    monto_col = find_col(gastos, ['Monto'])
    
    # Métricas actuales
    total_ventas = df_ventas[total_col].sum() if total_col else 0
    total_botellas = int(df_ventas[cant_col].sum()) if cant_col else 0
    n_trans = len(df_ventas)
    ticket_prom = total_ventas / n_trans if n_trans > 0 else 0
    total_gastos = gastos[monto_col].sum() if monto_col else 0
    utilidad = total_ventas - total_gastos
    margen = (utilidad / total_ventas * 100) if total_ventas > 0 else 0
    n_cotiz = len(df_cotiz)
    conversion = (n_trans / (n_trans + n_cotiz) * 100) if (n_trans + n_cotiz) > 0 else 0
    
    # Métricas periodo anterior para deltas reales
    total_ventas_prev = df_ventas_prev[total_col].sum() if total_col and not df_ventas_prev.empty else 0
    total_botellas_prev = int(df_ventas_prev[cant_col].sum()) if cant_col and not df_ventas_prev.empty else 0
    n_trans_prev = len(df_ventas_prev)
    ticket_prom_prev = total_ventas_prev / n_trans_prev if n_trans_prev > 0 else 0
    utilidad_prev = total_ventas_prev - total_gastos  # Simplificado
    margen_prev = (utilidad_prev / total_ventas_prev * 100) if total_ventas_prev > 0 else 0
    
    # Calcular deltas
    delta_ventas = calc_delta(total_ventas, total_ventas_prev)
    delta_botellas = calc_delta(total_botellas, total_botellas_prev)
    delta_ticket = calc_delta(ticket_prom, ticket_prom_prev)
    delta_utilidad = calc_delta(utilidad, utilidad_prev)
    delta_margen = margen - margen_prev  # Diferencia absoluta en puntos
    delta_conversion = 0  # Requiere datos de cotizaciones previas
    
    # ========== HEADER ==========
    st.markdown(f'''<div class="main-header">
        <div>
            <div class="main-title">Dashboard de Ventas</div>
            <div class="main-subtitle">Yuku Savi · Mezcal Artesanal de Puebla | {periodo}</div>
        </div>
        <div style="font-size:11px; color:var(--text3);">Última actualización: {datetime.now().strftime('%H:%M')}</div>
    </div>''', unsafe_allow_html=True)
    
    # ========== TABS ==========
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "💰 Ventas", "📦 Inventario", "💸 Gastos"])
    
    # ==================== TAB 1: OVERVIEW ====================
    with tab1:
        # KPIs con deltas reales
        cols = st.columns(6)
        with cols[0]: st.markdown(html_kpi("Ventas Totales", total_ventas, delta=delta_ventas, accent=True, large=True), unsafe_allow_html=True)
        with cols[1]: st.markdown(html_kpi("Utilidad Bruta", utilidad, delta=delta_utilidad), unsafe_allow_html=True)
        with cols[2]: st.markdown(html_kpi("Margen", margen, prefix="", suffix="%", delta=delta_margen, delta_label="pts"), unsafe_allow_html=True)
        with cols[3]: st.markdown(html_kpi("Botellas", total_botellas, prefix="", delta=delta_botellas), unsafe_allow_html=True)
        with cols[4]: st.markdown(html_kpi("Ticket Prom.", ticket_prom, delta=delta_ticket), unsafe_allow_html=True)
        with cols[5]: st.markdown(html_kpi("Conversión", conversion, prefix="", suffix="%", delta=delta_conversion), unsafe_allow_html=True)
        
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        
        # Row 2: Gráficos principales
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            st.markdown('<div class="card"><div class="card-title">📈 VENTAS VS META POR MES</div>', unsafe_allow_html=True)
            fig = chart_bars_meta(df_ventas, fecha_col, total_col, META_MENSUAL)
            if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="card"><div class="card-title">🎯 META DEL MES</div>', unsafe_allow_html=True)
            st.plotly_chart(chart_gauge(total_ventas, META_MENSUAL), use_container_width=True, config={'displayModeBar': False})
            st.markdown(f'<div style="text-align:center; color:var(--text3); font-size:11px;">${total_ventas:,.0f} de ${META_MENSUAL:,.0f}</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="card"><div class="card-title">📊 VENTAS POR CANAL</div>', unsafe_allow_html=True)
            if 'Canal' in df_ventas.columns and total_col:
                canal_data = df_ventas.groupby('Canal')[total_col].sum().sort_values(ascending=False)
                if not canal_data.empty:
                    total_c = canal_data.sum()
                    st.plotly_chart(chart_donut(canal_data.index.tolist(), canal_data.values.tolist(), f"${total_c/1000:.0f}k"), use_container_width=True, config={'displayModeBar': False})
                    st.markdown(html_legend([{'name': k, 'pct': (v/total_c)*100} for k, v in canal_data.items()], [C['accent'], C['blue'], C['purple'], C['amber']]), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        
        # Row 3: Gráficos avanzados
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="card"><div class="card-title">🗺️ TREEMAP DE PRODUCTOS</div>', unsafe_allow_html=True)
            prod_col = find_col(df_ventas, ['Producto'])
            fig_tree = chart_treemap(df_ventas, prod_col, total_col)
            if fig_tree: st.plotly_chart(fig_tree, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="card"><div class="card-title">🔥 HEATMAP VENTAS POR DÍA</div>', unsafe_allow_html=True)
            fig_heat = chart_heatmap(df_ventas, fecha_col, total_col)
            if fig_heat: st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        
        # Row 4: Área tendencia + Pipeline
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown('<div class="card"><div class="card-title">📈 TENDENCIA ACUMULADA</div>', unsafe_allow_html=True)
            fig_area = chart_area_tendencia(df_ventas, fecha_col, total_col)
            if fig_area: st.plotly_chart(fig_area, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="card"><div class="card-title">🎯 PIPELINE DE VENTAS</div>', unsafe_allow_html=True)
            if status_col:
                pipeline = ['Cotizado', 'Apartado', 'Pagado', 'Entregado']
                funnel_data = [{'etapa': s, 'count': len(ventas[ventas[status_col] == s])} for s in pipeline]
                st.markdown(html_funnel(funnel_data), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        
        # Row 5: Vendedores + Inventario
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="card"><div class="card-title">🗺️ VENTAS POR VENDEDOR</div>', unsafe_allow_html=True)
            if 'Vendedor' in df_ventas.columns and total_col:
                vend_data = df_ventas.groupby('Vendedor')[total_col].sum().sort_values(ascending=False)
                if not vend_data.empty:
                    total_v = vend_data.sum()
                    st.plotly_chart(chart_donut(vend_data.index.tolist(), vend_data.values.tolist(), f"{len(vend_data)}"), use_container_width=True, config={'displayModeBar': False})
                    st.markdown(html_legend([{'name': k, 'pct': (v/total_v)*100} for k, v in vend_data.items()], [C['accent'], C['blue'], C['purple'], C['amber'], C['red']]), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="card"><div class="card-title">📦 ESTADO DE INVENTARIO</div>', unsafe_allow_html=True)
            if not inventario.empty:
                prod_inv = find_col(inventario, ['Producto'])
                stock_col_inv = find_col(inventario, ['Stock Actual'])
                min_col = find_col(inventario, ['Stock Mínimo'])
                if prod_inv and stock_col_inv:
                    inv_data = [{'producto': r[prod_inv], 'stock': r[stock_col_inv], 'minimo': r[min_col] if min_col else 10} for _, r in inventario.head(6).iterrows()]
                    st.markdown(html_inventory(inv_data), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== TAB 2: VENTAS ====================
    with tab2:
        # Controles: Búsqueda + Ordenamiento + Exportar
        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
        with c1:
            search_ventas = st.text_input("🔍 Buscar", placeholder="Cliente, producto, folio...", key="search_ventas")
        with c2:
            sort_options = ["Fecha", "Total", "Cliente", "Producto"]
            sort_by = st.selectbox("Ordenar por", sort_options, key="sort_ventas")
        with c3:
            sort_order = st.selectbox("Orden", ["Descendente", "Ascendente"], key="order_ventas")
        with c4:
            st.markdown("<div style='height:27px;'></div>", unsafe_allow_html=True)
            excel_data, ext = to_excel(df_ventas)
            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if ext == 'xlsx' else "text/csv"
            st.download_button(f"📥 {ext.upper()}", excel_data, f"ventas_yukusavi.{ext}", mime, use_container_width=True)
        
        # Aplicar filtros
        df_display = df_ventas.copy()
        if search_ventas:
            df_display = search_dataframe(df_display, search_ventas, ['Folio', 'Cliente', 'Producto', 'Canal'])
        
        sort_col_map = {"Fecha": fecha_col, "Total": total_col, "Cliente": "Cliente", "Producto": "Producto"}
        if sort_by in sort_col_map and sort_col_map[sort_by]:
            df_display = sort_dataframe(df_display, sort_col_map[sort_by], ascending=(sort_order == "Ascendente"))
        
        st.markdown(f'''<div class="stats-row">
            <div class="stat-chip"><span class="stat-chip-value">{len(df_display)}</span><span class="stat-chip-label">Resultados</span></div>
            <div class="stat-chip"><span class="stat-chip-value">${df_display[total_col].sum() if total_col else 0:,.0f}</span><span class="stat-chip-label">Total</span></div>
            <div class="stat-chip"><span class="stat-chip-value">{int(df_display[cant_col].sum()) if cant_col else 0}</span><span class="stat-chip-label">Botellas</span></div>
        </div>''', unsafe_allow_html=True)
        
        st.markdown('<div class="card"><div class="card-title">📋 DETALLE DE VENTAS</div>', unsafe_allow_html=True)
        st.markdown(html_table_ventas(df_display.head(100), fecha_col, total_col, cant_col, status_col, search_ventas), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if len(df_display) > 100:
            st.info(f"Mostrando 100 de {len(df_display)} registros.")
    
    # ==================== TAB 3: INVENTARIO ====================
    with tab3:
        if not inventario.empty:
            prod_inv = find_col(inventario, ['Producto'])
            stock_col_inv = find_col(inventario, ['Stock Actual'])
            min_col = find_col(inventario, ['Stock Mínimo'])
            precio_col = find_col(inventario, ['Precio Venta'])
            
            # Export button
            c1, c2 = st.columns([4, 1])
            with c2:
                excel_inv, ext = to_excel(inventario)
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if ext == 'xlsx' else "text/csv"
                st.download_button(f"📥 {ext.upper()}", excel_inv, f"inventario_yukusavi.{ext}", mime, use_container_width=True)
            
            total_stock = int(inventario[stock_col_inv].sum()) if stock_col_inv else 0
            valor_inv = (inventario[stock_col_inv] * inventario[precio_col]).sum() if stock_col_inv and precio_col else 0
            productos_bajo = len(inventario[inventario[stock_col_inv] <= inventario[min_col]]) if stock_col_inv and min_col else 0
            
            st.markdown(f'''<div class="stats-row">
                <div class="stat-chip"><span class="stat-chip-value">{len(inventario)}</span><span class="stat-chip-label">Productos</span></div>
                <div class="stat-chip"><span class="stat-chip-value">{total_stock}</span><span class="stat-chip-label">Unidades</span></div>
                <div class="stat-chip"><span class="stat-chip-value">${valor_inv:,.0f}</span><span class="stat-chip-label">Valor</span></div>
                <div class="stat-chip"><span class="stat-chip-value" style="color: {C['red'] if productos_bajo > 0 else C['green']};">{productos_bajo}</span><span class="stat-chip-label">Stock Bajo</span></div>
            </div>''', unsafe_allow_html=True)
            
            st.markdown('<div class="card"><div class="card-title">📦 ESTADO POR PRODUCTO</div>', unsafe_allow_html=True)
            st.markdown(html_inventory_cards(inventario, prod_inv, stock_col_inv, min_col), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="card"><div class="card-title">📊 DISTRIBUCIÓN DE STOCK</div>', unsafe_allow_html=True)
                if prod_inv and stock_col_inv:
                    stock_data = inventario.set_index(prod_inv)[stock_col_inv].sort_values(ascending=False)
                    st.plotly_chart(chart_donut(stock_data.index.tolist(), stock_data.values.tolist(), f"{total_stock}"), use_container_width=True, config={'displayModeBar': False})
                st.markdown('</div>', unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="card"><div class="card-title">⚠️ ALERTAS DE STOCK</div>', unsafe_allow_html=True)
                if prod_inv and stock_col_inv and min_col:
                    alertas = inventario[inventario[stock_col_inv] <= inventario[min_col]]
                    if not alertas.empty:
                        inv_data = [{'producto': r[prod_inv], 'stock': r[stock_col_inv], 'minimo': r[min_col]} for _, r in alertas.iterrows()]
                        st.markdown(html_inventory(inv_data), unsafe_allow_html=True)
                    else:
                        st.markdown('<p style="color: var(--green); text-align: center; padding: 20px;">✓ Todo el inventario está en niveles óptimos</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No hay datos de inventario")
    
    # ==================== TAB 4: GASTOS ====================
    with tab4:
        if not gastos.empty:
            fecha_gasto_col = find_col(gastos, ['Fecha'])
            cat_col = find_col(gastos, ['Categoría', 'Categoria'])
            monto_col_g = find_col(gastos, ['Monto'])
            
            # Controles
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                search_gastos = st.text_input("🔍 Buscar", placeholder="Categoría, concepto, proveedor...", key="search_gastos")
            with c2:
                sort_gastos = st.selectbox("Ordenar por", ["Fecha", "Monto", "Categoría"], key="sort_gastos")
            with c3:
                st.markdown("<div style='height:27px;'></div>", unsafe_allow_html=True)
                excel_gastos, ext = to_excel(gastos)
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if ext == 'xlsx' else "text/csv"
                st.download_button(f"📥 {ext.upper()}", excel_gastos, f"gastos_yukusavi.{ext}", mime, use_container_width=True)
            
            # Aplicar filtros
            df_gastos_display = gastos.copy()
            if search_gastos:
                df_gastos_display = search_dataframe(df_gastos_display, search_gastos, [cat_col or '', 'Concepto', 'Descripción', 'Proveedor'])
            
            sort_g_map = {"Fecha": fecha_gasto_col, "Monto": monto_col_g, "Categoría": cat_col}
            if sort_gastos in sort_g_map and sort_g_map[sort_gastos]:
                df_gastos_display = sort_dataframe(df_gastos_display, sort_g_map[sort_gastos], ascending=False)
            
            total_gastos_tab = df_gastos_display[monto_col_g].sum() if monto_col_g else 0
            n_gastos = len(df_gastos_display)
            gasto_prom = total_gastos_tab / n_gastos if n_gastos > 0 else 0
            n_categorias = df_gastos_display[cat_col].nunique() if cat_col else 0
            
            st.markdown(f'''<div class="stats-row">
                <div class="stat-chip"><span class="stat-chip-value">{n_gastos}</span><span class="stat-chip-label">Registros</span></div>
                <div class="stat-chip"><span class="stat-chip-value">${total_gastos_tab:,.0f}</span><span class="stat-chip-label">Total</span></div>
                <div class="stat-chip"><span class="stat-chip-value">${gasto_prom:,.0f}</span><span class="stat-chip-label">Promedio</span></div>
                <div class="stat-chip"><span class="stat-chip-value">{n_categorias}</span><span class="stat-chip-label">Categorías</span></div>
            </div>''', unsafe_allow_html=True)
            
            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown('<div class="card"><div class="card-title">📊 GASTOS POR CATEGORÍA</div>', unsafe_allow_html=True)
                fig_gastos = chart_gastos_categoria(df_gastos_display, cat_col, monto_col_g)
                if fig_gastos:
                    st.plotly_chart(fig_gastos, use_container_width=True, config={'displayModeBar': False})
                st.markdown('</div>', unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="card"><div class="card-title">🥧 DISTRIBUCIÓN</div>', unsafe_allow_html=True)
                if cat_col and monto_col_g:
                    cat_data = df_gastos_display.groupby(cat_col)[monto_col_g].sum().sort_values(ascending=False)
                    total_cat = cat_data.sum()
                    if total_cat > 0:
                        st.plotly_chart(chart_donut(cat_data.index.tolist(), cat_data.values.tolist(), f"${total_cat/1000:.0f}k"), use_container_width=True, config={'displayModeBar': False})
                        st.markdown(html_legend([{'name': k, 'pct': (v/total_cat)*100} for k, v in cat_data.items()], [C['accent'], C['blue'], C['purple'], C['amber'], C['red']]), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="card"><div class="card-title">📋 DETALLE DE GASTOS</div>', unsafe_allow_html=True)
            st.markdown(html_table_gastos(df_gastos_display.head(50), fecha_gasto_col, cat_col, monto_col_g, search_gastos), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No hay datos de gastos")
    
    # ========== FOOTER ==========
    st.markdown(f'''<div class="main-footer">
        🌵 <strong style="color:{C['text2']};">Yuku Savi</strong> · Dashboard de Inteligencia de Negocio · 
        <span style="color:{C['accent']}; font-weight:600;">SINAPSIS</span>
    </div>''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
