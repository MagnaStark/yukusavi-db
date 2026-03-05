import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import calendar

# ============================================
# CONFIGURACIÓN
# ============================================
st.set_page_config(
    page_title="Yuku Savi | Dashboard Ejecutivo",
    page_icon="🌵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Google Sheets
SHEET_ID = "169pU5z_xFWBACaXBkTogQzgV15L9cxJZ9kZXvr7dXG8"
STATUS_VENTAS = ['Entregado', 'Pagado', 'Apartado']
STATUS_COTIZACIONES = ['Cotizado']

# ============================================
# PALETA DE COLORES PREMIUM YUKU SAVI
# ============================================
COLORS = {
    'bg_dark': '#0d0b08',
    'bg_card': '#1a1611',
    'bg_card_hover': '#252015',
    'border': '#3d3526',
    'border_gold': '#c9a22740',
    'text_primary': '#f5f0e8',
    'text_secondary': '#a69882',
    'text_muted': '#6b5d4d',
    'gold': '#c9a227',
    'gold_light': '#e8c84a',
    'amber': '#d4883a',
    'green': '#7c9a5e',
    'green_light': '#9ab87a',
    'red': '#b54a3c',
    'red_light': '#d4665a',
    'purple': '#8b6b9c',
    'blue': '#5a8a9c',
    'cream': '#f0e6d3',
}

# ============================================
# CSS PREMIUM
# ============================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Montserrat:wght@300;400;500;600;700&display=swap');

:root {{
    --gold: {COLORS['gold']};
    --amber: {COLORS['amber']};
    --bg-dark: {COLORS['bg_dark']};
    --bg-card: {COLORS['bg_card']};
}}

* {{ font-family: 'Montserrat', sans-serif !important; }}
h1, h2, h3, .serif {{ font-family: 'Cormorant Garamond', serif !important; }}

.stApp {{
    background: radial-gradient(ellipse at top, #1a1611 0%, {COLORS['bg_dark']} 50%, #080705 100%);
}}

/* Efecto de partículas/textura */
.stApp::before {{
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    opacity: 0.03;
    pointer-events: none;
    z-index: 0;
}}

/* Header Premium */
.header-premium {{
    background: linear-gradient(135deg, rgba(26,22,17,0.95) 0%, rgba(13,11,8,0.98) 100%);
    padding: 2.5rem 3rem;
    border-radius: 24px;
    margin-bottom: 2rem;
    border: 1px solid {COLORS['border_gold']};
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
}}
.header-premium::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, {COLORS['gold']}, {COLORS['amber']}, {COLORS['gold']}, transparent);
    animation: shimmer 3s ease-in-out infinite;
}}
.header-premium::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 200px;
    height: 1px;
    background: linear-gradient(90deg, transparent, {COLORS['gold']}40, transparent);
}}
@keyframes shimmer {{
    0%, 100% {{ opacity: 0.5; }}
    50% {{ opacity: 1; }}
}}
.header-title {{
    color: {COLORS['cream']};
    font-size: 2.5rem;
    font-weight: 600;
    margin: 0;
    font-family: 'Cormorant Garamond', serif !important;
    letter-spacing: 3px;
    text-transform: uppercase;
}}
.header-subtitle {{
    color: {COLORS['gold']};
    font-size: 1rem;
    margin: 0.5rem 0 0 0;
    font-style: italic;
    letter-spacing: 2px;
}}
.header-badge {{
    position: absolute;
    top: 1.5rem;
    right: 2rem;
    background: linear-gradient(135deg, {COLORS['gold']}, {COLORS['amber']});
    color: {COLORS['bg_dark']};
    padding: 0.5rem 1.2rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

/* Métricas Premium */
.metric-grid {{
    display: grid;
    gap: 1.25rem;
}}
.metric-card {{
    background: linear-gradient(145deg, {COLORS['bg_card']} 0%, rgba(13,11,8,0.8) 100%);
    border-radius: 20px;
    padding: 1.5rem;
    border: 1px solid {COLORS['border']};
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}}
.metric-card:hover {{
    transform: translateY(-4px);
    border-color: {COLORS['gold']}60;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4), 0 0 30px {COLORS['gold']}10;
}}
.metric-card.featured {{
    background: linear-gradient(145deg, {COLORS['gold']}12 0%, {COLORS['amber']}08 100%);
    border-color: {COLORS['gold']}40;
}}
.metric-card.featured::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, {COLORS['gold']}, {COLORS['amber']}, {COLORS['gold']});
}}
.metric-icon {{
    width: 48px;
    height: 48px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, {COLORS['gold']}20, {COLORS['amber']}10);
    border: 1px solid {COLORS['gold']}30;
}}
.metric-label {{
    color: {COLORS['text_secondary']};
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 0.5rem;
}}
.metric-value {{
    color: {COLORS['text_primary']};
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
    font-family: 'Cormorant Garamond', serif !important;
}}
.metric-card.featured .metric-value {{
    color: {COLORS['gold']};
    font-size: 2.2rem;
}}
.metric-delta {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 0.3rem 0.7rem;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 0.75rem;
}}
.metric-delta.up {{
    background: {COLORS['green']}20;
    color: {COLORS['green_light']};
}}
.metric-delta.down {{
    background: {COLORS['red']}20;
    color: {COLORS['red_light']};
}}
.metric-spark {{
    position: absolute;
    bottom: 1rem;
    right: 1rem;
    opacity: 0.3;
}}

/* Cards Premium */
.card-premium {{
    background: linear-gradient(145deg, {COLORS['bg_card']} 0%, rgba(13,11,8,0.9) 100%);
    border-radius: 20px;
    padding: 1.75rem;
    border: 1px solid {COLORS['border']};
    margin-bottom: 1.25rem;
    position: relative;
}}
.card-premium::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 2rem;
    right: 2rem;
    height: 1px;
    background: linear-gradient(90deg, transparent, {COLORS['gold']}30, transparent);
}}
.card-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid {COLORS['border']};
}}
.card-title {{
    color: {COLORS['text_primary']};
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}
.card-title-icon {{
    width: 32px;
    height: 32px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, {COLORS['gold']}20, transparent);
    border: 1px solid {COLORS['gold']}30;
    font-size: 0.9rem;
}}
.card-badge {{
    background: {COLORS['gold']}15;
    color: {COLORS['gold']};
    padding: 0.35rem 0.8rem;
    border-radius: 8px;
    font-size: 0.7rem;
    font-weight: 600;
    border: 1px solid {COLORS['gold']}30;
}}

/* Sidebar Premium */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {COLORS['bg_card']} 0%, {COLORS['bg_dark']} 100%) !important;
    border-right: 1px solid {COLORS['border']} !important;
}}
.sidebar-brand {{
    text-align: center;
    padding: 2rem 1.5rem;
    background: linear-gradient(180deg, {COLORS['bg_card']} 0%, transparent 100%);
    border-radius: 20px;
    margin-bottom: 2rem;
    border: 1px solid {COLORS['border_gold']};
    position: relative;
}}
.sidebar-brand::after {{
    content: '';
    position: absolute;
    bottom: -1px;
    left: 20%;
    right: 20%;
    height: 1px;
    background: linear-gradient(90deg, transparent, {COLORS['gold']}, transparent);
}}
.sidebar-logo {{
    font-size: 3rem;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0 0 20px {COLORS['gold']}40);
}}
.sidebar-title {{
    color: {COLORS['cream']};
    font-size: 1.6rem;
    font-weight: 600;
    font-family: 'Cormorant Garamond', serif !important;
    letter-spacing: 4px;
    margin: 0;
}}
.sidebar-tagline {{
    color: {COLORS['gold']};
    font-size: 0.6rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 0.3rem;
}}
.sidebar-section {{
    margin-bottom: 1.5rem;
}}
.sidebar-section-title {{
    color: {COLORS['text_secondary']};
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 1rem;
    padding-left: 0.5rem;
    border-left: 2px solid {COLORS['gold']};
}}

/* Status Indicators Premium */
.status-card {{
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: linear-gradient(135deg, {COLORS['bg_card']} 0%, rgba(13,11,8,0.5) 100%);
    border-radius: 14px;
    border: 1px solid {COLORS['border']};
    margin-bottom: 0.75rem;
    transition: all 0.3s ease;
}}
.status-card:hover {{
    border-color: {COLORS['gold']}40;
    transform: translateX(4px);
}}
.status-indicator {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
    position: relative;
}}
.status-indicator::after {{
    content: '';
    position: absolute;
    inset: -4px;
    border-radius: 50%;
    border: 2px solid currentColor;
    opacity: 0.3;
}}
.status-indicator.green {{ background: {COLORS['green']}; color: {COLORS['green']}; box-shadow: 0 0 15px {COLORS['green']}60; }}
.status-indicator.amber {{ background: {COLORS['amber']}; color: {COLORS['amber']}; box-shadow: 0 0 15px {COLORS['amber']}60; }}
.status-indicator.red {{ background: {COLORS['red']}; color: {COLORS['red']}; box-shadow: 0 0 15px {COLORS['red']}60; }}
.status-label {{ color: {COLORS['text_muted']}; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px; }}
.status-value {{ color: {COLORS['text_primary']}; font-size: 0.95rem; font-weight: 600; }}

/* Tabs Premium */
.stTabs [data-baseweb="tab-list"] {{
    gap: 8px;
    background: {COLORS['bg_card']};
    padding: 0.5rem;
    border-radius: 16px;
    border: 1px solid {COLORS['border']};
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent;
    border-radius: 12px;
    padding: 0.8rem 1.5rem;
    color: {COLORS['text_secondary']};
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
}}
.stTabs [data-baseweb="tab"]:hover {{
    color: {COLORS['text_primary']};
    background: {COLORS['border']}40;
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {COLORS['gold']}, {COLORS['amber']}) !important;
    color: {COLORS['bg_dark']} !important;
    box-shadow: 0 4px 15px {COLORS['gold']}40;
}}

/* Inventory Item Premium */
.inv-item {{
    display: flex;
    align-items: center;
    gap: 1.25rem;
    padding: 1.25rem;
    background: linear-gradient(135deg, {COLORS['bg_card']} 0%, rgba(13,11,8,0.5) 100%);
    border-radius: 16px;
    border: 1px solid {COLORS['border']};
    margin-bottom: 0.75rem;
    transition: all 0.3s ease;
}}
.inv-item:hover {{
    border-color: {COLORS['gold']}50;
    transform: translateX(8px);
    box-shadow: -8px 0 20px {COLORS['gold']}10;
}}
.inv-bottle {{
    font-size: 2rem;
    filter: drop-shadow(0 0 10px {COLORS['gold']}30);
}}
.inv-details {{ flex: 1; }}
.inv-name {{
    color: {COLORS['text_primary']};
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
}}
.inv-agave {{
    display: inline-block;
    background: {COLORS['green']}20;
    color: {COLORS['green_light']};
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-size: 0.65rem;
    font-weight: 600;
    border: 1px solid {COLORS['green']}30;
    margin-left: 0.5rem;
}}
.inv-stock {{
    color: {COLORS['gold']};
    font-size: 1.4rem;
    font-weight: 700;
    font-family: 'Cormorant Garamond', serif !important;
}}
.inv-stock-label {{
    color: {COLORS['text_muted']};
    font-size: 0.65rem;
    text-transform: uppercase;
}}
.inv-bar {{
    height: 6px;
    background: {COLORS['border']};
    border-radius: 3px;
    margin-top: 0.75rem;
    overflow: hidden;
}}
.inv-fill {{
    height: 100%;
    border-radius: 3px;
    transition: width 0.5s ease;
}}
.inv-fill.good {{ background: linear-gradient(90deg, {COLORS['green']}, {COLORS['green_light']}); }}
.inv-fill.warning {{ background: linear-gradient(90deg, {COLORS['amber']}, {COLORS['gold']}); }}
.inv-fill.danger {{ background: linear-gradient(90deg, {COLORS['red']}, {COLORS['red_light']}); }}

/* Top Products Premium */
.top-item {{
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    margin-bottom: 0.75rem;
    background: linear-gradient(135deg, transparent 0%, {COLORS['bg_card']}50 100%);
    border-radius: 12px;
    transition: all 0.3s ease;
}}
.top-item:hover {{
    background: {COLORS['bg_card']};
}}
.top-rank {{
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1rem;
    font-family: 'Cormorant Garamond', serif !important;
}}
.top-rank.gold {{
    background: linear-gradient(135deg, {COLORS['gold']}, {COLORS['amber']});
    color: {COLORS['bg_dark']};
    box-shadow: 0 4px 15px {COLORS['gold']}40;
}}
.top-rank.silver {{
    background: linear-gradient(135deg, #8b8b8b, #a8a8a8);
    color: {COLORS['bg_dark']};
}}
.top-rank.bronze {{
    background: linear-gradient(135deg, #8b6b4a, #a67c52);
    color: {COLORS['cream']};
}}
.top-progress {{
    height: 8px;
    background: {COLORS['border']};
    border-radius: 4px;
    margin-top: 0.5rem;
    overflow: hidden;
}}
.top-progress-fill {{
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, {COLORS['gold']}, {COLORS['amber']}, {COLORS['gold']});
    background-size: 200% 100%;
    animation: progressShine 2s ease infinite;
}}
@keyframes progressShine {{
    0% {{ background-position: 200% 0; }}
    100% {{ background-position: -200% 0; }}
}}

/* Funnel Premium */
.funnel-item {{
    margin-bottom: 0.75rem;
}}
.funnel-bar {{
    padding: 1rem 1.25rem;
    border-radius: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: {COLORS['cream']};
    font-weight: 600;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}}
.funnel-bar::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    transform: translateX(-100%);
    transition: transform 0.5s ease;
}}
.funnel-bar:hover::before {{
    transform: translateX(100%);
}}
.funnel-count {{
    background: rgba(0,0,0,0.3);
    padding: 0.3rem 0.8rem;
    border-radius: 8px;
    font-size: 0.9rem;
}}

/* Footer Premium */
.footer-premium {{
    text-align: center;
    padding: 2.5rem;
    margin-top: 3rem;
    border-top: 1px solid {COLORS['border']};
    position: relative;
}}
.footer-premium::before {{
    content: '';
    position: absolute;
    top: -1px;
    left: 25%;
    right: 25%;
    height: 1px;
    background: linear-gradient(90deg, transparent, {COLORS['gold']}50, transparent);
}}
.footer-brand {{
    font-size: 1.2rem;
    font-family: 'Cormorant Garamond', serif !important;
    color: {COLORS['cream']};
    letter-spacing: 3px;
}}
.footer-credit {{
    color: {COLORS['text_muted']};
    font-size: 0.75rem;
    margin-top: 0.5rem;
}}
.footer-credit span {{
    color: {COLORS['gold']};
    font-weight: 600;
}}

/* Hide Streamlit */
#MainMenu, footer, .stDeployButton {{ display: none !important; }}

/* Selectbox styling */
.stSelectbox > div > div {{
    background: {COLORS['bg_card']} !important;
    border-color: {COLORS['border']} !important;
    border-radius: 10px !important;
}}
.stSelectbox > div > div:hover {{
    border-color: {COLORS['gold']}50 !important;
}}

/* Multiselect styling */
.stMultiSelect > div > div {{
    background: {COLORS['bg_card']} !important;
    border-color: {COLORS['border']} !important;
    border-radius: 10px !important;
}}

/* Button styling */
.stButton > button {{
    background: linear-gradient(135deg, {COLORS['gold']}, {COLORS['amber']}) !important;
    color: {COLORS['bg_dark']} !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}}
.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px {COLORS['gold']}40 !important;
}}

/* Dataframe styling */
.stDataFrame {{
    border-radius: 12px;
    overflow: hidden;
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
    if pd.isna(v): return 0
    if isinstance(v, (int, float)): return float(v)
    try: return float(str(v).replace('$','').replace(',','').strip())
    except: return 0

@st.cache_data(ttl=60)
def load_sheet(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

def load_all_data():
    ventas = load_sheet("VENTAS")
    inventario = load_sheet("INVENTARIO")
    produccion = load_sheet("PRODUCCION")
    gastos = load_sheet("GASTOS")
    return ventas, inventario, produccion, gastos

def process_ventas(df):
    if df.empty: return df
    df = df.copy()
    for c in ['Precio Unitario', 'Subtotal', 'Total', 'Costo Envío', 'Cantidad']:
        if c in df.columns: df[c] = df[c].apply(clean_money)
    fc = find_col(df, ['Fecha'])
    if fc: df[fc] = pd.to_datetime(df[fc], errors='coerce')
    return df

def process_gastos(df):
    if df.empty: return df
    df = df.copy()
    mc = find_col(df, ['Monto'])
    if mc: df[mc] = df[mc].apply(clean_money)
    fc = find_col(df, ['Fecha'])
    if fc: df[fc] = pd.to_datetime(df[fc], errors='coerce')
    return df

def process_inventario(df):
    if df.empty: return df
    df = df.copy()
    for c in ['Stock Actual', 'Stock Mínimo', 'Stock Máximo', 'Costo Producción', 'Precio Venta']:
        if c in df.columns: df[c] = df[c].apply(clean_money)
    return df

def filter_by_date(df, periodo, fecha_col):
    if df.empty or not fecha_col: return df
    df = df.copy()
    df[fecha_col] = pd.to_datetime(df[fecha_col], errors='coerce')
    today = datetime.now()
    
    if periodo == "Hoy":
        return df[df[fecha_col].dt.date == today.date()]
    elif periodo == "Esta semana":
        start = today - timedelta(days=today.weekday())
        return df[df[fecha_col].dt.date >= start.date()]
    elif periodo == "Este mes":
        return df[(df[fecha_col].dt.month == today.month) & (df[fecha_col].dt.year == today.year)]
    elif periodo == "Mes anterior":
        last_month = today.replace(day=1) - timedelta(days=1)
        return df[(df[fecha_col].dt.month == last_month.month) & (df[fecha_col].dt.year == last_month.year)]
    elif periodo == "Este trimestre":
        quarter = (today.month - 1) // 3
        start_month = quarter * 3 + 1
        return df[(df[fecha_col].dt.month >= start_month) & (df[fecha_col].dt.month < start_month + 3) & (df[fecha_col].dt.year == today.year)]
    elif periodo == "Este año":
        return df[df[fecha_col].dt.year == today.year]
    return df

# ============================================
# COMPONENTES UI
# ============================================
def metric_card(icon, label, value, prefix="$", delta=None, featured=False):
    delta_html = ""
    if delta is not None:
        cls = "up" if delta >= 0 else "down"
        arrow = "↑" if delta >= 0 else "↓"
        delta_html = f'<div class="metric-delta {cls}">{arrow} {abs(delta):.1f}%</div>'
    
    val_str = f"${value:,.0f}" if prefix == "$" else f"{value:.1f}%" if prefix == "%" else f"{value:,.0f}"
    card_class = "metric-card featured" if featured else "metric-card"
    
    return f'''
    <div class="{card_class}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{val_str}</div>
        {delta_html}
    </div>
    '''

def status_indicator(label, value, status):
    return f'''
    <div class="status-card">
        <div class="status-indicator {status}"></div>
        <div>
            <div class="status-label">{label}</div>
            <div class="status-value">{value}</div>
        </div>
    </div>
    '''

# ============================================
# GRÁFICOS PREMIUM
# ============================================
def chart_ventas_trend(df):
    if df.empty: return None
    fc = find_col(df, ['Fecha'])
    tc = find_col(df, ['Total'])
    if not fc or not tc: return None
    
    df_temp = df.copy()
    df_temp['_fecha'] = pd.to_datetime(df_temp[fc], errors='coerce')
    df_temp['_total'] = pd.to_numeric(df_temp[tc], errors='coerce').fillna(0)
    daily = df_temp.groupby(df_temp['_fecha'].dt.date)['_total'].sum().reset_index()
    daily.columns = ['fecha', 'total']
    daily = daily.sort_values('fecha')
    
    fig = go.Figure()
    
    # Área con gradiente
    fig.add_trace(go.Scatter(
        x=daily['fecha'], y=daily['total'],
        fill='tozeroy',
        line=dict(color=COLORS['gold'], width=3, shape='spline'),
        fillcolor='rgba(201, 162, 39, 0.1)',
        hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>'
    ))
    
    # Puntos
    fig.add_trace(go.Scatter(
        x=daily['fecha'], y=daily['total'],
        mode='markers',
        marker=dict(
            size=10,
            color=COLORS['gold'],
            line=dict(width=2, color=COLORS['bg_dark'])
        ),
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text_secondary'], family='Montserrat'),
        margin=dict(l=50, r=20, t=20, b=40),
        height=300,
        showlegend=False,
        yaxis=dict(
            tickformat='$,.0f',
            gridcolor=COLORS['border'],
            gridwidth=0.5,
            zeroline=False
        ),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0)',
            zeroline=False
        ),
        hovermode='x unified'
    )
    return fig

def chart_gauge_premium(value, max_val, title):
    pct = min((value / max_val) * 100, 100) if max_val > 0 else 0
    
    if pct >= 80:
        color = COLORS['green']
    elif pct >= 50:
        color = COLORS['amber']
    else:
        color = COLORS['red']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct,
        number={
            'suffix': '%',
            'font': {'size': 48, 'color': COLORS['cream'], 'family': 'Cormorant Garamond'}
        },
        gauge={
            'axis': {
                'range': [0, 100],
                'tickwidth': 0,
                'tickcolor': 'rgba(0,0,0,0)',
                'tickfont': {'color': 'rgba(0,0,0,0)'}
            },
            'bar': {'color': color, 'thickness': 0.8},
            'bgcolor': COLORS['border'],
            'borderwidth': 0,
            'steps': [
                {'range': [0, 50], 'color': 'rgba(181, 74, 60, 0.1)'},
                {'range': [50, 80], 'color': 'rgba(212, 136, 58, 0.1)'},
                {'range': [80, 100], 'color': 'rgba(124, 154, 94, 0.1)'}
            ]
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=220,
        margin=dict(l=30, r=30, t=40, b=20),
        font=dict(family='Montserrat')
    )
    return fig

def chart_canal_premium(df):
    if df.empty: return None
    cc = find_col(df, ['Canal'])
    tc = find_col(df, ['Total'])
    if not cc or not tc: return None
    
    df_temp = df.copy()
    df_temp['_total'] = pd.to_numeric(df_temp[tc], errors='coerce').fillna(0)
    by_canal = df_temp.groupby(cc)['_total'].sum().sort_values(ascending=True)
    
    colors = [COLORS['amber'], COLORS['gold'], COLORS['green']]
    
    fig = go.Figure(go.Bar(
        y=by_canal.index,
        x=by_canal.values,
        orientation='h',
        marker=dict(
            color=colors[-len(by_canal):],
            line=dict(width=0)
        ),
        text=[f'${v:,.0f}' for v in by_canal.values],
        textposition='outside',
        textfont=dict(color=COLORS['text_primary'], size=12, family='Montserrat'),
        hovertemplate='<b>%{y}</b><br>$%{x:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text_secondary'], family='Montserrat'),
        margin=dict(l=100, r=80, t=20, b=20),
        height=200,
        yaxis=dict(gridcolor='rgba(0,0,0,0)'),
        xaxis=dict(
            tickformat='$,.0f',
            gridcolor=COLORS['border'],
            gridwidth=0.5
        ),
        bargap=0.4
    )
    return fig

def chart_gastos_donut(df):
    if df.empty: return None
    cc = find_col(df, ['Categoría', 'Categoria'])
    mc = find_col(df, ['Monto'])
    if not cc or not mc: return None
    
    df_temp = df.copy()
    df_temp['_monto'] = pd.to_numeric(df_temp[mc], errors='coerce').fillna(0)
    by_cat = df_temp.groupby(cc)['_monto'].sum().sort_values(ascending=False)
    
    colors = [COLORS['gold'], COLORS['amber'], COLORS['green'], COLORS['purple'], 
              COLORS['blue'], COLORS['text_secondary'], COLORS['red']]
    
    fig = go.Figure(go.Pie(
        labels=by_cat.index,
        values=by_cat.values,
        hole=0.65,
        marker=dict(colors=colors[:len(by_cat)], line=dict(color=COLORS['bg_dark'], width=2)),
        textinfo='percent',
        textfont=dict(color=COLORS['cream'], size=11, family='Montserrat'),
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text_secondary'], family='Montserrat'),
        margin=dict(l=20, r=20, t=20, b=20),
        height=280,
        showlegend=False,
        annotations=[dict(
            text=f'${by_cat.sum():,.0f}',
            x=0.5, y=0.5,
            font=dict(size=20, color=COLORS['gold'], family='Cormorant Garamond'),
            showarrow=False
        )]
    )
    return fig

def chart_vendedor_premium(df):
    if df.empty: return None
    vc = find_col(df, ['Vendedor'])
    tc = find_col(df, ['Total'])
    if not vc or not tc: return None
    
    df_temp = df.copy()
    df_temp['_total'] = pd.to_numeric(df_temp[tc], errors='coerce').fillna(0)
    by_vend = df_temp.groupby(vc)['_total'].sum().sort_values(ascending=True).tail(5)
    
    fig = go.Figure(go.Bar(
        y=by_vend.index,
        x=by_vend.values,
        orientation='h',
        marker=dict(
            color=COLORS['gold'],
            line=dict(width=0)
        ),
        text=[f'${v:,.0f}' for v in by_vend.values],
        textposition='outside',
        textfont=dict(color=COLORS['text_primary'], size=11, family='Montserrat')
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text_secondary'], family='Montserrat'),
        margin=dict(l=80, r=60, t=20, b=20),
        height=220,
        yaxis=dict(gridcolor='rgba(0,0,0,0)'),
        xaxis=dict(tickformat='$,.0f', gridcolor=COLORS['border'], gridwidth=0.5),
        bargap=0.35
    )
    return fig

# ============================================
# MAIN
# ============================================
def main():
    # Cargar datos
    with st.spinner("🌵 Cargando datos..."):
        ventas_raw, inventario_raw, produccion_raw, gastos_raw = load_all_data()
    
    ventas = process_ventas(ventas_raw)
    gastos = process_gastos(gastos_raw)
    inventario = process_inventario(inventario_raw)
    
    if ventas.empty:
        st.error("⚠️ No se pudieron cargar los datos")
        st.info("Verifica que el Google Sheets sea público")
        return
    
    # ============================================
    # SIDEBAR
    # ============================================
    with st.sidebar:
        st.markdown('''
        <div class="sidebar-brand">
            <div class="sidebar-logo">🌵</div>
            <div class="sidebar-title">YUKU SAVI</div>
            <div class="sidebar-tagline">Mezcal Artesanal</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Botón actualizar
        if st.button("🔄 Actualizar Datos", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        
        # FILTROS
        st.markdown('<div class="sidebar-section-title">📅 Periodo</div>', unsafe_allow_html=True)
        periodo = st.selectbox(
            "Periodo",
            ["Todo", "Hoy", "Esta semana", "Este mes", "Mes anterior", "Este trimestre", "Este año"],
            index=3,
            label_visibility="collapsed"
        )
        
        st.markdown('<div class="sidebar-section-title">🎯 Filtros</div>', unsafe_allow_html=True)
        
        # Filtro de canal
        canales = ["Todos"] + sorted(ventas['Canal'].dropna().unique().tolist()) if 'Canal' in ventas.columns else ["Todos"]
        canal_filter = st.selectbox("Canal", canales, label_visibility="collapsed")
        
        # Filtro de vendedor
        vendedores = ["Todos"] + sorted(ventas['Vendedor'].dropna().unique().tolist()) if 'Vendedor' in ventas.columns else ["Todos"]
        vendedor_filter = st.selectbox("Vendedor", vendedores, label_visibility="collapsed")
        
        # Filtro de producto
        productos = ["Todos"] + sorted(ventas['Producto'].dropna().unique().tolist()) if 'Producto' in ventas.columns else ["Todos"]
        producto_filter = st.selectbox("Producto", productos, label_visibility="collapsed")
        
        st.markdown("---")
        
        # APLICAR FILTROS
        df_filtered = ventas.copy()
        
        # Filtro de fecha
        fc = find_col(df_filtered, ['Fecha'])
        if periodo != "Todo" and fc:
            df_filtered = filter_by_date(df_filtered, periodo, fc)
        
        # Filtro de canal
        if canal_filter != "Todos" and 'Canal' in df_filtered.columns:
            df_filtered = df_filtered[df_filtered['Canal'] == canal_filter]
        
        # Filtro de vendedor
        if vendedor_filter != "Todos" and 'Vendedor' in df_filtered.columns:
            df_filtered = df_filtered[df_filtered['Vendedor'] == vendedor_filter]
        
        # Filtro de producto
        if producto_filter != "Todos" and 'Producto' in df_filtered.columns:
            df_filtered = df_filtered[df_filtered['Producto'] == producto_filter]
        
        # Separar ventas y cotizaciones
        sc = find_col(df_filtered, ['Status'])
        df_ventas = df_filtered[df_filtered[sc].isin(STATUS_VENTAS)] if sc else df_filtered
        df_cot = df_filtered[df_filtered[sc].isin(STATUS_COTIZACIONES)] if sc else pd.DataFrame()
        
        # Calcular métricas
        tc = find_col(df_ventas, ['Total'])
        cc = find_col(df_ventas, ['Cantidad'])
        
        total_ventas = pd.to_numeric(df_ventas[tc], errors='coerce').fillna(0).sum() if tc else 0
        total_botellas = int(pd.to_numeric(df_ventas[cc], errors='coerce').fillna(0).sum()) if cc else 0
        n_ventas = len(df_ventas)
        ticket_prom = total_ventas / n_ventas if n_ventas > 0 else 0
        
        mc = find_col(gastos, ['Monto'])
        total_gastos = pd.to_numeric(gastos[mc], errors='coerce').fillna(0).sum() if mc else 0
        
        utilidad = total_ventas - total_gastos
        margen = (utilidad / total_ventas * 100) if total_ventas > 0 else 0
        meta = 300000
        
        # STATUS INDICATORS
        st.markdown('<div class="sidebar-section-title">🚦 Estado</div>', unsafe_allow_html=True)
        
        pct_meta = (total_ventas / meta * 100) if meta > 0 else 0
        meta_status = "green" if pct_meta >= 80 else "amber" if pct_meta >= 50 else "red"
        st.markdown(status_indicator("Meta Mensual", f"{pct_meta:.0f}%", meta_status), unsafe_allow_html=True)
        
        inv_bajo = 0
        if not inventario.empty:
            stock_col = find_col(inventario, ['Stock Actual'])
            min_col = find_col(inventario, ['Stock Mínimo'])
            if stock_col and min_col:
                inv_bajo = len(inventario[inventario[stock_col] <= inventario[min_col]])
        inv_status = "red" if inv_bajo > 2 else "amber" if inv_bajo > 0 else "green"
        st.markdown(status_indicator("Inventario", f"{inv_bajo} bajo stock", inv_status), unsafe_allow_html=True)
        
        margin_status = "green" if margen >= 30 else "amber" if margen >= 15 else "red"
        st.markdown(status_indicator("Margen", f"{margen:.1f}%", margin_status), unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f'''
        <div style="text-align:center;padding:1rem;">
            <div style="color:{COLORS['text_muted']};font-size:0.65rem;margin-bottom:0.3rem;">Desarrollado por</div>
            <div style="color:{COLORS['gold']};font-weight:600;font-size:0.9rem;letter-spacing:2px;">SINAPSIS</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # ============================================
    # MAIN CONTENT
    # ============================================
    
    # Header
    st.markdown(f'''
    <div class="header-premium">
        <div class="header-badge">LIVE</div>
        <h1 class="header-title">🌵 Yuku Savi</h1>
        <p class="header-subtitle">Dashboard Ejecutivo • {periodo}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Métricas principales
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card("💰", "Ventas Totales", total_ventas, delta=12.5, featured=True), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("📦", "Botellas Vendidas", total_botellas, prefix=""), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("📈", "Utilidad Bruta", utilidad, featured=True), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card("📊", "Margen", margen, prefix="%"), unsafe_allow_html=True)
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(metric_card("🛒", "Transacciones", n_ventas, prefix=""), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("🎫", "Ticket Promedio", ticket_prom), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("📝", "Cotizaciones", len(df_cot), prefix=""), unsafe_allow_html=True)
    with c4:
        st.markdown(metric_card("💸", "Gastos", total_gastos), unsafe_allow_html=True)
    with c5:
        st.markdown(metric_card("🌵", "SKUs Activos", len(inventario) if not inventario.empty else 0, prefix=""), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        f"📊 Overview",
        f"💰 Ventas ({n_ventas})",
        f"📦 Inventario",
        f"💸 Gastos"
    ])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f'''
            <div class="card-premium">
                <div class="card-header">
                    <div class="card-title">
                        <div class="card-title-icon">📈</div>
                        Tendencia de Ventas
                    </div>
                    <div class="card-badge">{periodo}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            fig = chart_ventas_trend(df_ventas)
            if fig: st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f'''
            <div class="card-premium">
                <div class="card-header">
                    <div class="card-title">
                        <div class="card-title-icon">🎯</div>
                        Meta del Mes
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            fig = chart_gauge_premium(total_ventas, meta, "Meta")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f'<p style="text-align:center;color:{COLORS["text_secondary"]};font-size:0.85rem;margin-top:-1rem;">${total_ventas:,.0f} / ${meta:,.0f}</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'''
            <div class="card-premium">
                <div class="card-header">
                    <div class="card-title">
                        <div class="card-title-icon">🏆</div>
                        Top Mezcales
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            pc = find_col(df_ventas, ['Producto'])
            tc = find_col(df_ventas, ['Total'])
            if pc and tc and not df_ventas.empty:
                df_temp = df_ventas.copy()
                df_temp['_total'] = pd.to_numeric(df_temp[tc], errors='coerce').fillna(0)
                top = df_temp.groupby(pc)['_total'].sum().sort_values(ascending=False).head(5)
                mx = top.max() if len(top) > 0 else 1
                
                for i, (prod, val) in enumerate(top.items()):
                    pct = (val / mx * 100) if mx > 0 else 0
                    rank_class = "gold" if i == 0 else "silver" if i == 1 else "bronze"
                    st.markdown(f'''
                    <div class="top-item">
                        <div class="top-rank {rank_class}">{i+1}</div>
                        <div style="flex:1;">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <span style="color:{COLORS['text_primary']};font-weight:500;">{prod}</span>
                                <span style="color:{COLORS['gold']};font-weight:700;font-family:'Cormorant Garamond',serif;">${val:,.0f}</span>
                            </div>
                            <div class="top-progress">
                                <div class="top-progress-fill" style="width:{pct}%;"></div>
                            </div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="card-premium">
                <div class="card-header">
                    <div class="card-title">
                        <div class="card-title-icon">📊</div>
                        Ventas por Canal
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            fig = chart_canal_premium(df_ventas)
            if fig: st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'''
            <div class="card-premium">
                <div class="card-header">
                    <div class="card-title">
                        <div class="card-title-icon">🎯</div>
                        Embudo de Ventas
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            funnel_data = [
                ('Cotizado', COLORS['text_secondary'], 100),
                ('Apartado', COLORS['amber'], 80),
                ('Pagado', COLORS['gold'], 60),
                ('Entregado', COLORS['green'], 40)
            ]
            
            sc = find_col(ventas, ['Status'])
            for status, color, width in funnel_data:
                if sc:
                    df_s = ventas[ventas[sc] == status]
                    cnt = len(df_s)
                    tc = find_col(df_s, ['Total'])
                    monto = pd.to_numeric(df_s[tc], errors='coerce').fillna(0).sum() if tc else 0
                else:
                    cnt = 0
                    monto = 0
                
                st.markdown(f'''
                <div class="funnel-item">
                    <div class="funnel-bar" style="width:{width}%;background:linear-gradient(135deg,{color}dd,{color}88);">
                        <span>{status}</span>
                        <span class="funnel-count">{cnt} · ${monto:,.0f}</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="card-premium">
                <div class="card-header">
                    <div class="card-title">
                        <div class="card-title-icon">👤</div>
                        Por Vendedor
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            fig = chart_vendedor_premium(df_ventas)
            if fig: st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown(f'''
        <div class="card-premium">
            <div class="card-header">
                <div class="card-title">
                    <div class="card-title-icon">📋</div>
                    Detalle de Ventas
                </div>
                <div class="card-badge">{len(df_ventas)} registros</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        if not df_ventas.empty:
            st.dataframe(df_ventas, hide_index=True, use_container_width=True)
    
    with tab3:
        if inventario.empty:
            st.info("No hay datos de inventario")
        else:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f'''
                <div class="card-premium">
                    <div class="card-header">
                        <div class="card-title">
                            <div class="card-title-icon">🍾</div>
                            Inventario de Mezcales
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
                
                prod_col = find_col(inventario, ['Producto'])
                agave_col = find_col(inventario, ['Tipo Agave'])
                stock_col = find_col(inventario, ['Stock Actual'])
                min_col = find_col(inventario, ['Stock Mínimo'])
                max_col = find_col(inventario, ['Stock Máximo'])
                
                if prod_col and stock_col:
                    for _, row in inventario.iterrows():
                        stock = row[stock_col] if stock_col else 0
                        min_s = row[min_col] if min_col else 0
                        max_s = row[max_col] if max_col else 100
                        pct = (stock / max_s * 100) if max_s > 0 else 0
                        fill_class = "danger" if stock <= min_s else "warning" if pct < 50 else "good"
                        agave = row[agave_col] if agave_col else ""
                        
                        st.markdown(f'''
                        <div class="inv-item">
                            <div class="inv-bottle">🍾</div>
                            <div class="inv-details">
                                <div>
                                    <span class="inv-name">{row[prod_col]}</span>
                                    <span class="inv-agave">{agave}</span>
                                </div>
                                <div class="inv-bar">
                                    <div class="inv-fill {fill_class}" style="width:{pct}%;"></div>
                                </div>
                            </div>
                            <div style="text-align:right;">
                                <div class="inv-stock">{int(stock)}</div>
                                <div class="inv-stock-label">unidades</div>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                precio_col = find_col(inventario, ['Precio Venta'])
                costo_col = find_col(inventario, ['Costo Producción'])
                if stock_col and precio_col:
                    valor_inv = (inventario[stock_col] * inventario[precio_col]).sum()
                    costo_inv = (inventario[stock_col] * inventario[costo_col]).sum() if costo_col else 0
                    
                    st.markdown(f'''
                    <div class="card-premium">
                        <div class="card-header">
                            <div class="card-title">
                                <div class="card-title-icon">💰</div>
                                Valor del Inventario
                            </div>
                        </div>
                        <div style="margin-top:1rem;">
                            <div style="display:flex;justify-content:space-between;padding:0.75rem 0;border-bottom:1px solid {COLORS['border']};">
                                <span style="color:{COLORS['text_secondary']};">Precio venta</span>
                                <span style="color:{COLORS['gold']};font-weight:700;font-size:1.2rem;font-family:'Cormorant Garamond',serif;">${valor_inv:,.0f}</span>
                            </div>
                            <div style="display:flex;justify-content:space-between;padding:0.75rem 0;border-bottom:1px solid {COLORS['border']};">
                                <span style="color:{COLORS['text_secondary']};">Costo</span>
                                <span style="color:{COLORS['text_primary']};font-weight:600;">${costo_inv:,.0f}</span>
                            </div>
                            <div style="display:flex;justify-content:space-between;padding:0.75rem 0;">
                                <span style="color:{COLORS['text_secondary']};">Utilidad potencial</span>
                                <span style="color:{COLORS['green']};font-weight:700;font-size:1.1rem;">${valor_inv-costo_inv:,.0f}</span>
                            </div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
    
    with tab4:
        if gastos.empty:
            st.info("No hay datos de gastos")
        else:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown(f'''
                <div class="card-premium">
                    <div class="card-header">
                        <div class="card-title">
                            <div class="card-title-icon">📊</div>
                            Distribución de Gastos
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                fig = chart_gastos_donut(gastos)
                if fig: st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown(f'''
                <div class="card-premium">
                    <div class="card-header">
                        <div class="card-title">
                            <div class="card-title-icon">📋</div>
                            Por Categoría
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
                
                cc = find_col(gastos, ['Categoría', 'Categoria'])
                mc = find_col(gastos, ['Monto'])
                if cc and mc:
                    gastos_temp = gastos.copy()
                    gastos_temp['_monto'] = pd.to_numeric(gastos_temp[mc], errors='coerce').fillna(0)
                    by_cat = gastos_temp.groupby(cc)['_monto'].sum().sort_values(ascending=False)
                    total_g = by_cat.sum()
                    
                    for cat, monto in by_cat.items():
                        pct = (monto / total_g * 100) if total_g > 0 else 0
                        st.markdown(f'''
                        <div style="display:flex;justify-content:space-between;align-items:center;padding:0.75rem 0;border-bottom:1px solid {COLORS['border']};">
                            <span style="color:{COLORS['text_primary']};font-size:0.9rem;">{cat}</span>
                            <div>
                                <span style="color:{COLORS['gold']};font-weight:700;margin-right:0.75rem;">${monto:,.0f}</span>
                                <span style="color:{COLORS['text_muted']};font-size:0.8rem;">({pct:.0f}%)</span>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="card-premium">
                <div class="card-header">
                    <div class="card-title">
                        <div class="card-title-icon">📋</div>
                        Detalle de Gastos
                    </div>
                    <div class="card-badge">{len(gastos)} registros</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            st.dataframe(gastos, hide_index=True, use_container_width=True)
    
    # Footer
    st.markdown(f'''
    <div class="footer-premium">
        <div class="footer-brand">🌵 YUKU SAVI</div>
        <div class="footer-credit">
            Mezcal Artesanal de Puebla • Dashboard por <span>SINAPSIS</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
