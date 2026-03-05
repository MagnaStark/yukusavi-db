import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ============================================
# CONFIGURACIÓN
# ============================================
st.set_page_config(
    page_title="Yuku Savi | Dashboard",
    page_icon="🌵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Google Sheets - Yuku Savi
SHEET_ID = "169pU5z_xFWBACaXBkTogQzgV15L9cxJZ9kZXvr7dXG8"

# GIDs de cada hoja (Google Sheets los asigna automáticamente)
# Si el dashboard no carga bien, ve a cada hoja en tu Sheets y copia el gid= de la URL
GID_VENTAS = "0"
GID_INVENTARIO = "1721aborar"  # Placeholder - se detectará automáticamente
GID_PRODUCCION = "2"
GID_GASTOS = "3"
GID_MATERIALES = "4"

STATUS_VENTAS = ['Entregado', 'Pagado', 'Apartado']
STATUS_COTIZACIONES = ['Cotizado']

# ============================================
# COLORES YUKU SAVI
# ============================================
COLORS = {
    'bg': '#1a1611',
    'card': '#2a2319',
    'border': '#3d3526',
    'text': '#f5f0e8',
    'text2': '#a69882',
    'gold': '#c9a227',
    'amber': '#d4883a',
    'green': '#7c9a5e',
    'red': '#b54a3c',
    'brown': '#8b6b4a',
    'cream': '#f0e6d3',
}

# ============================================
# CSS
# ============================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Montserrat:wght@300;400;500;600;700&display=swap');

* {{ font-family: 'Montserrat', sans-serif !important; }}
h1, h2, h3, .title {{ font-family: 'Playfair Display', serif !important; }}

.stApp {{ background: linear-gradient(180deg, {COLORS['bg']} 0%, #0f0d0a 100%); }}

.header {{
    background: linear-gradient(135deg, #2a2319 0%, #1a1611 50%, #2a2319 100%);
    padding: 2rem 2.5rem; border-radius: 20px; margin-bottom: 1.5rem;
    border: 1px solid {COLORS['gold']}30; position: relative; overflow: hidden;
}}
.header::before {{
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, transparent, {COLORS['gold']}, {COLORS['amber']}, transparent);
}}
.header h1 {{ 
    color: {COLORS['cream']}; font-size: 2rem; font-weight: 600; margin: 0;
    font-family: 'Playfair Display', serif !important; letter-spacing: 1px;
}}
.header p {{ color: {COLORS['gold']}; margin: 0.4rem 0 0 0; font-size: 0.9rem; font-style: italic; }}

.metric {{
    background: linear-gradient(145deg, {COLORS['card']} 0%, #1f1a14 100%);
    border-radius: 16px; padding: 1.15rem; border: 1px solid {COLORS['border']};
    margin-bottom: 0.75rem; transition: all 0.3s ease;
}}
.metric:hover {{ transform: translateY(-3px); border-color: {COLORS['gold']}50; box-shadow: 0 8px 25px rgba(0,0,0,0.3); }}
.metric.gold {{ 
    background: linear-gradient(135deg, {COLORS['gold']}15 0%, {COLORS['amber']}10 100%);
    border-color: {COLORS['gold']}50;
}}
.metric-label {{ 
    color: {COLORS['text2']}; font-size: 0.68rem; font-weight: 600; 
    text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 0.35rem;
}}
.metric-value {{ color: {COLORS['cream']}; font-size: 1.5rem; font-weight: 700; }}
.metric.gold .metric-value {{ color: {COLORS['gold']}; }}
.metric-delta {{ 
    display: inline-flex; align-items: center; gap: 0.2rem;
    padding: 0.15rem 0.45rem; border-radius: 6px; font-size: 0.7rem; 
    font-weight: 600; margin-top: 0.35rem;
}}
.metric-delta.up {{ background: {COLORS['green']}25; color: {COLORS['green']}; }}
.metric-delta.down {{ background: {COLORS['red']}25; color: {COLORS['red']}; }}

.card {{
    background: linear-gradient(145deg, {COLORS['card']} 0%, #1f1a14 100%);
    border-radius: 16px; padding: 1.35rem; border: 1px solid {COLORS['border']};
    margin-bottom: 1rem;
}}
.card-title {{ 
    color: {COLORS['text2']}; font-size: 0.7rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;
}}

.sidebar-logo {{
    text-align: center; padding: 1.5rem 1rem;
    background: linear-gradient(145deg, #2a2319 0%, #1a1611 100%);
    border-radius: 16px; margin-bottom: 1.5rem;
    border: 1px solid {COLORS['gold']}30; position: relative;
}}
.sidebar-logo::before {{
    content: ''; position: absolute; top: 0; left: 50%; transform: translateX(-50%);
    width: 50%; height: 2px;
    background: linear-gradient(90deg, transparent, {COLORS['gold']}, transparent);
}}

.status {{ 
    display: flex; align-items: center; gap: 0.6rem; padding: 0.65rem;
    background: {COLORS['card']}; border-radius: 10px; 
    border: 1px solid {COLORS['border']}; margin-bottom: 0.5rem;
}}
.status-dot {{ width: 10px; height: 10px; border-radius: 50%; }}
.status-dot.green {{ background: {COLORS['green']}; box-shadow: 0 0 8px {COLORS['green']}80; }}
.status-dot.amber {{ background: {COLORS['amber']}; box-shadow: 0 0 8px {COLORS['amber']}80; }}
.status-dot.red {{ background: {COLORS['red']}; box-shadow: 0 0 8px {COLORS['red']}80; }}

.inv-item {{
    display: flex; align-items: center; gap: 1rem; padding: 0.85rem;
    background: {COLORS['card']}; border-radius: 10px;
    border: 1px solid {COLORS['border']}; margin-bottom: 0.6rem;
}}
.inv-bar {{ height: 4px; background: {COLORS['border']}; border-radius: 2px; margin-top: 0.3rem; }}
.inv-fill {{ height: 100%; border-radius: 2px; }}
.inv-fill.good {{ background: linear-gradient(90deg, {COLORS['green']}, {COLORS['green']}aa); }}
.inv-fill.warning {{ background: linear-gradient(90deg, {COLORS['amber']}, {COLORS['amber']}aa); }}
.inv-fill.danger {{ background: linear-gradient(90deg, {COLORS['red']}, {COLORS['red']}aa); }}

.agave-badge {{
    display: inline-block; padding: 0.25rem 0.6rem; border-radius: 6px;
    font-size: 0.65rem; font-weight: 600; background: {COLORS['green']}20;
    color: {COLORS['green']}; border: 1px solid {COLORS['green']}40;
    margin-left: 8px;
}}

.funnel {{ margin-bottom: 0.6rem; }}
.funnel-bar {{ 
    padding: 0.65rem 0.9rem; border-radius: 8px; 
    display: flex; justify-content: space-between; 
    color: {COLORS['cream']}; font-weight: 600; font-size: 0.8rem;
}}

.top-prod {{ display: flex; align-items: center; gap: 0.9rem; margin-bottom: 0.9rem; }}
.top-rank {{ 
    width: 30px; height: 30px; border-radius: 8px; 
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.85rem;
}}
.top-rank.gold {{ background: {COLORS['gold']}; color: #1a1611; }}
.top-rank.silver {{ background: {COLORS['brown']}; color: {COLORS['cream']}; }}
.progress {{ height: 5px; background: {COLORS['border']}; border-radius: 3px; margin-top: 0.35rem; }}
.progress-fill {{ height: 100%; border-radius: 3px; background: linear-gradient(90deg, {COLORS['gold']}, {COLORS['amber']}); }}

.footer {{ 
    text-align: center; padding: 1.5rem; color: {COLORS['text2']}; 
    font-size: 0.7rem; margin-top: 2rem; border-top: 1px solid {COLORS['border']};
}}

.stTabs [data-baseweb="tab-list"] {{ 
    gap: 6px; background: {COLORS['card']}; padding: 0.4rem; 
    border-radius: 14px; border: 1px solid {COLORS['border']};
}}
.stTabs [data-baseweb="tab"] {{ 
    background: transparent; border-radius: 10px; padding: 0.65rem 1.1rem;
    color: {COLORS['text2']}; font-weight: 600; font-size: 0.8rem;
}}
.stTabs [aria-selected="true"] {{ 
    background: linear-gradient(135deg, {COLORS['gold']}, {COLORS['amber']}) !important;
    color: #1a1611 !important;
}}

#MainMenu, footer, .stDeployButton {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNCIONES
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
def load_sheet_by_name(sheet_name):
    """Carga una hoja por nombre usando la URL de exportación"""
    # Intentar cargar por nombre de hoja
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.warning(f"No se pudo cargar {sheet_name}: {e}")
        return pd.DataFrame()

def load_all_data():
    """Carga todas las hojas necesarias"""
    ventas = load_sheet_by_name("VENTAS")
    inventario = load_sheet_by_name("INVENTARIO")
    produccion = load_sheet_by_name("PRODUCCION")
    gastos = load_sheet_by_name("GASTOS")
    materiales = load_sheet_by_name("MATERIALES")
    return ventas, inventario, produccion, gastos, materiales

def process_ventas(df):
    if df.empty: return df
    for c in ['Precio Unitario', 'Subtotal', 'Total', 'Costo Envío']:
        if c in df.columns: df[c] = df[c].apply(clean_money)
    fc = find_col(df, ['Fecha'])
    if fc: df[fc] = pd.to_datetime(df[fc], errors='coerce')
    return df

def process_gastos(df):
    if df.empty: return df
    mc = find_col(df, ['Monto'])
    if mc: df[mc] = df[mc].apply(clean_money)
    fc = find_col(df, ['Fecha'])
    if fc: df[fc] = pd.to_datetime(df[fc], errors='coerce')
    return df

def process_inventario(df):
    if df.empty: return df
    for c in ['Stock Actual', 'Stock Mínimo', 'Stock Máximo', 'Costo Producción', 'Precio Venta']:
        if c in df.columns: df[c] = df[c].apply(clean_money)
    return df

def get_ventas(df):
    sc = find_col(df, ['Status'])
    return df[df[sc].isin(STATUS_VENTAS)] if sc else df

def get_cotizaciones(df):
    sc = find_col(df, ['Status'])
    return df[df[sc].isin(STATUS_COTIZACIONES)] if sc else pd.DataFrame()

def calc_total(df):
    if df.empty: return 0
    tc = find_col(df, ['Total'])
    return pd.to_numeric(df[tc], errors='coerce').fillna(0).sum() if tc else 0

def calc_gastos(df):
    if df.empty: return 0
    mc = find_col(df, ['Monto'])
    return pd.to_numeric(df[mc], errors='coerce').fillna(0).sum() if mc else 0

def calc_botellas(df):
    if df.empty: return 0
    cc = find_col(df, ['Cantidad'])
    return int(pd.to_numeric(df[cc], errors='coerce').fillna(0).sum()) if cc else 0

def metric(label, value, prefix="$", delta=None, gold=False):
    d = ""
    if delta is not None:
        cls = "up" if delta >= 0 else "down"
        icon = "↑" if delta >= 0 else "↓"
        d = f'<span class="metric-delta {cls}">{icon} {abs(delta):.1f}%</span>'
    v = f"${value:,.0f}" if prefix == "$" else f"{value:.1f}%" if prefix == "%" else f"{value:,.0f}"
    c = "metric gold" if gold else "metric"
    st.markdown(f'<div class="{c}"><div class="metric-label">{label}</div><div class="metric-value">{v}</div>{d}</div>', unsafe_allow_html=True)

# ============================================
# GRÁFICOS
# ============================================
def chart_ventas(df):
    if df.empty: return None
    fc = find_col(df, ['Fecha'])
    tc = find_col(df, ['Total'])
    if not fc or not tc: return None
    
    df_temp = df.copy()
    df_temp['_fecha'] = pd.to_datetime(df_temp[fc], errors='coerce')
    df_temp['_total'] = pd.to_numeric(df_temp[tc], errors='coerce').fillna(0)
    daily = df_temp.groupby(df_temp['_fecha'].dt.date)['_total'].sum().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily['_fecha'], y=daily['_total'],
        fill='tozeroy', line=dict(color=COLORS['gold'], width=3),
        fillcolor=f"rgba(201, 162, 39, 0.15)"
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text2']), margin=dict(l=50, r=20, t=20, b=40),
        height=280, yaxis=dict(tickformat='$,.0f', gridcolor=COLORS['border']),
        xaxis=dict(gridcolor=COLORS['border']), hovermode='x'
    )
    return fig

def chart_gauge(value, max_val):
    pct = min((value / max_val) * 100, 100) if max_val > 0 else 0
    color = COLORS['green'] if pct >= 80 else COLORS['amber'] if pct >= 50 else COLORS['red']
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=pct,
        number={'suffix': '%', 'font': {'size': 32, 'color': COLORS['cream']}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 0, 'tickcolor': 'rgba(0,0,0,0)'},
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': COLORS['border'], 'borderwidth': 0
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=170, margin=dict(l=20, r=20, t=30, b=10)
    )
    return fig

def chart_canal(df):
    if df.empty: return None
    cc = find_col(df, ['Canal'])
    tc = find_col(df, ['Total'])
    if not cc or not tc: return None
    
    df_temp = df.copy()
    df_temp['_total'] = pd.to_numeric(df_temp[tc], errors='coerce').fillna(0)
    by_canal = df_temp.groupby(cc)['_total'].sum().sort_values(ascending=True)
    
    fig = go.Figure(go.Bar(
        y=by_canal.index, x=by_canal.values, orientation='h',
        marker=dict(color=[COLORS['gold'], COLORS['amber'], COLORS['brown']][-len(by_canal):]),
        text=[f'${v:,.0f}' for v in by_canal.values], textposition='outside'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text2']), margin=dict(l=80, r=50, t=20, b=20),
        height=200, yaxis=dict(gridcolor=COLORS['border']),
        xaxis=dict(tickformat='$,.0f', gridcolor=COLORS['border'])
    )
    return fig

def chart_gastos_cat(df):
    if df.empty: return None
    cc = find_col(df, ['Categoría', 'Categoria'])
    mc = find_col(df, ['Monto'])
    if not cc or not mc: return None
    
    df_temp = df.copy()
    df_temp['_monto'] = pd.to_numeric(df_temp[mc], errors='coerce').fillna(0)
    by_cat = df_temp.groupby(cc)['_monto'].sum().sort_values(ascending=False)
    
    colors_pie = [COLORS['gold'], COLORS['amber'], COLORS['brown'], COLORS['green'], 
                  COLORS['text2'], COLORS['border'], COLORS['red']]
    fig = go.Figure(go.Pie(
        labels=by_cat.index, values=by_cat.values, hole=0.6,
        marker=dict(colors=colors_pie[:len(by_cat)]),
        textinfo='percent', textfont=dict(color=COLORS['cream'], size=11)
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', font=dict(color=COLORS['text2']),
        margin=dict(l=20, r=20, t=20, b=20), height=260, showlegend=False
    )
    return fig

# ============================================
# MAIN
# ============================================
def main():
    # Load data
    with st.spinner("🌵 Cargando datos de Yuku Savi..."):
        ventas_raw, inventario_raw, produccion_raw, gastos_raw, materiales_raw = load_all_data()
    
    ventas = process_ventas(ventas_raw.copy())
    gastos = process_gastos(gastos_raw.copy())
    inventario = process_inventario(inventario_raw.copy())
    
    if ventas.empty:
        st.error("⚠️ No se pudieron cargar los datos. Verifica que el Google Sheets sea público.")
        st.info("Ve a tu Sheets → Compartir → Cambiar a 'Cualquier persona con el enlace' → Lector")
        return
    
    df_ventas = get_ventas(ventas)
    df_cot = get_cotizaciones(ventas)
    
    # Métricas
    total_ventas = calc_total(df_ventas)
    total_gastos = calc_gastos(gastos)
    total_botellas = calc_botellas(df_ventas)
    n_ventas = len(df_ventas)
    ticket_prom = total_ventas / n_ventas if n_ventas > 0 else 0
    utilidad = total_ventas - total_gastos
    margen = (utilidad / total_ventas * 100) if total_ventas > 0 else 0
    meta = 300000
    
    # Sidebar
    with st.sidebar:
        st.markdown(f'''
        <div class="sidebar-logo">
            <div style="font-size:2.2rem;">🌵</div>
            <h2 style="color:{COLORS['cream']};font-size:1.4rem;font-weight:600;margin:0.5rem 0 0 0;letter-spacing:2px;font-family:'Playfair Display',serif;">YUKU SAVI</h2>
            <p style="color:{COLORS['gold']};font-size:0.6rem;letter-spacing:3px;margin:0.2rem 0 0 0;">MEZCAL ARTESANAL</p>
        </div>
        ''', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔄", use_container_width=True, help="Actualizar"):
                st.cache_data.clear()
                st.rerun()
        with c2:
            st.button("🌙", use_container_width=True)
        
        st.markdown("---")
        st.markdown("**📅 Periodo**")
        periodo = st.selectbox("", ["Todo", "Este mes", "Mes anterior", "Trimestre"], label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown("**🚦 Estado del Negocio**")
        
        pct_meta = (total_ventas / meta * 100) if meta > 0 else 0
        dot_class = "green" if pct_meta >= 80 else "amber" if pct_meta >= 50 else "red"
        st.markdown(f'''
        <div class="status">
            <div class="status-dot {dot_class}"></div>
            <div>
                <div style="color:{COLORS['text2']};font-size:0.65rem;">META MENSUAL</div>
                <div style="color:{COLORS['cream']};font-size:0.85rem;font-weight:600;">{pct_meta:.0f}%</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Inventario bajo
        inv_bajo = 0
        if not inventario.empty:
            stock_col = find_col(inventario, ['Stock Actual'])
            min_col = find_col(inventario, ['Stock Mínimo'])
            if stock_col and min_col:
                inv_bajo = len(inventario[inventario[stock_col] <= inventario[min_col]])
        
        dot_inv = "red" if inv_bajo > 2 else "amber" if inv_bajo > 0 else "green"
        st.markdown(f'''
        <div class="status">
            <div class="status-dot {dot_inv}"></div>
            <div>
                <div style="color:{COLORS['text2']};font-size:0.65rem;">INVENTARIO</div>
                <div style="color:{COLORS['cream']};font-size:0.85rem;font-weight:600;">{inv_bajo} bajo stock</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f'''
        <div style="text-align:center;opacity:0.6;">
            <p style="font-size:0.6rem;color:{COLORS['text2']};margin:0;">Desarrollado por</p>
            <p style="color:{COLORS['gold']};font-weight:600;margin:0;">SINAPSIS</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Header
    st.markdown('''
    <div class="header">
        <h1>🌵 Yuku Savi Dashboard</h1>
        <p>¡Una ofrenda para los Dioses!</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Métricas principales
    c1, c2, c3, c4 = st.columns(4)
    with c1: metric("💰 Ventas Totales", total_ventas, delta=12.5)
    with c2: metric("📦 Botellas Vendidas", total_botellas, prefix="")
    with c3: metric("📈 Utilidad Bruta", utilidad, gold=True)
    with c4: metric("📊 Margen", margen, prefix="%")
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: metric("🛒 # Ventas", n_ventas, prefix="")
    with c2: metric("🎫 Ticket Prom", ticket_prom)
    with c3: metric("📝 Cotizaciones", len(df_cot), prefix="")
    with c4: metric("💸 Gastos", total_gastos)
    with c5: metric("🌵 Productos", len(inventario) if not inventario.empty else 0, prefix="")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", f"💰 Ventas ({n_ventas})", 
        "📦 Inventario", "🏭 Producción", "💸 Gastos"
    ])
    
    with tab1:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f'<div class="card"><div class="card-title">📈 Tendencia de Ventas</div></div>', unsafe_allow_html=True)
            fig = chart_ventas(df_ventas)
            if fig: st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown(f'<div class="card"><div class="card-title">🎯 Meta del Mes</div></div>', unsafe_allow_html=True)
            fig = chart_gauge(total_ventas, meta)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f'<p style="text-align:center;color:{COLORS["text2"]};font-size:0.75rem;margin-top:-10px;">${total_ventas:,.0f} / ${meta:,.0f}</p>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="card"><div class="card-title">🏆 Top Mezcales</div>', unsafe_allow_html=True)
            pc = find_col(df_ventas, ['Producto'])
            tc = find_col(df_ventas, ['Total'])
            if pc and tc and not df_ventas.empty:
                df_temp = df_ventas.copy()
                df_temp['_total'] = pd.to_numeric(df_temp[tc], errors='coerce').fillna(0)
                top = df_temp.groupby(pc)['_total'].sum().sort_values(ascending=False).head(5)
                mx = top.max() if len(top) > 0 else 1
                ranks = ['gold', 'silver', 'silver', 'silver', 'silver']
                for i, (prod, val) in enumerate(top.items()):
                    pct = (val / mx * 100) if mx > 0 else 0
                    st.markdown(f'''
                    <div class="top-prod">
                        <div class="top-rank {ranks[i] if i < len(ranks) else 'silver'}">{i+1}</div>
                        <div style="flex:1;">
                            <div style="display:flex;justify-content:space-between;">
                                <span style="color:{COLORS['cream']};font-size:0.85rem;">{prod}</span>
                                <span style="color:{COLORS['gold']};font-weight:600;">${val:,.0f}</span>
                            </div>
                            <div class="progress"><div class="progress-fill" style="width:{pct}%;"></div></div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with c2:
            st.markdown(f'<div class="card"><div class="card-title">📊 Ventas por Canal</div></div>', unsafe_allow_html=True)
            fig = chart_canal(df_ventas)
            if fig: st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown(f'<div class="card"><div class="card-title">📋 Detalle de Ventas</div></div>', unsafe_allow_html=True)
        if not df_ventas.empty:
            st.dataframe(df_ventas, hide_index=True, use_container_width=True)
    
    with tab3:
        if inventario.empty:
            st.info("No hay datos de inventario")
        else:
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f'<div class="card"><div class="card-title">🍾 Inventario de Mezcales</div>', unsafe_allow_html=True)
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
                            <div style="font-size:1.5rem;">🍾</div>
                            <div style="flex:1;">
                                <div style="display:flex;justify-content:space-between;align-items:center;">
                                    <div>
                                        <span style="color:{COLORS['cream']};font-size:0.85rem;font-weight:500;">{row[prod_col]}</span>
                                        <span class="agave-badge">{agave}</span>
                                    </div>
                                    <span style="color:{COLORS['gold']};font-size:0.9rem;font-weight:700;">{int(stock)} uds</span>
                                </div>
                                <div class="inv-bar"><div class="inv-fill {fill_class}" style="width:{pct}%;"></div></div>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with c2:
                # Valor del inventario
                precio_col = find_col(inventario, ['Precio Venta'])
                costo_col = find_col(inventario, ['Costo Producción'])
                if stock_col and precio_col:
                    valor_inv = (inventario[stock_col] * inventario[precio_col]).sum()
                    costo_inv = (inventario[stock_col] * inventario[costo_col]).sum() if costo_col else 0
                    
                    st.markdown(f'''
                    <div class="card">
                        <div class="card-title">💰 Valor del Inventario</div>
                        <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
                            <span style="color:{COLORS['text2']};">Precio venta:</span>
                            <span style="color:{COLORS['gold']};font-weight:600;">${valor_inv:,.0f}</span>
                        </div>
                        <div style="display:flex;justify-content:space-between;">
                            <span style="color:{COLORS['text2']};">Costo:</span>
                            <span style="color:{COLORS['cream']};">${costo_inv:,.0f}</span>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
    
    with tab4:
        if produccion_raw.empty:
            st.info("No hay datos de producción")
        else:
            st.markdown(f'<div class="card"><div class="card-title">🏭 Lotes en Producción</div></div>', unsafe_allow_html=True)
            st.dataframe(produccion_raw, hide_index=True, use_container_width=True)
    
    with tab5:
        if gastos.empty:
            st.info("No hay datos de gastos")
        else:
            c1, c2 = st.columns([1, 1])
            with c1:
                st.markdown(f'<div class="card"><div class="card-title">💸 Distribución de Gastos</div></div>', unsafe_allow_html=True)
                fig = chart_gastos_cat(gastos)
                if fig: st.plotly_chart(fig, use_container_width=True)
            
            with c2:
                st.markdown(f'<div class="card"><div class="card-title">📊 Por Categoría</div>', unsafe_allow_html=True)
                cc = find_col(gastos, ['Categoría', 'Categoria'])
                mc = find_col(gastos, ['Monto'])
                if cc and mc:
                    gastos['_monto'] = pd.to_numeric(gastos[mc], errors='coerce').fillna(0)
                    by_cat = gastos.groupby(cc)['_monto'].sum().sort_values(ascending=False)
                    total_g = by_cat.sum()
                    for cat, monto in by_cat.items():
                        pct = (monto / total_g * 100) if total_g > 0 else 0
                        st.markdown(f'''
                        <div style="display:flex;justify-content:space-between;align-items:center;padding:0.5rem 0;border-bottom:1px solid {COLORS['border']};">
                            <span style="color:{COLORS['cream']};font-size:0.8rem;">{cat}</span>
                            <div>
                                <span style="color:{COLORS['gold']};font-weight:600;margin-right:10px;">${monto:,.0f}</span>
                                <span style="color:{COLORS['text2']};font-size:0.75rem;">({pct:.0f}%)</span>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown(f'<div class="card"><div class="card-title">📋 Detalle de Gastos</div></div>', unsafe_allow_html=True)
            st.dataframe(gastos, hide_index=True, use_container_width=True)
    
    # Footer
    st.markdown(f'''
    <div class="footer">
        🌵 <b>Yuku Savi</b> | Mezcal Artesanal de Puebla<br>
        Dashboard desarrollado por <span style="color:{COLORS['gold']};font-weight:600;">SINAPSIS</span> | Transformación Digital
    </div>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
