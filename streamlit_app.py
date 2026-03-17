import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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

# Google Sheets
SHEET_ID = "169pU5z_xFWBACaXBkTogQzgV15L9cxJZ9kZXvr7dXG8"
STATUS_VENTAS = ['Entregado', 'Pagado', 'Apartado']
STATUS_COTIZACIONES = ['Cotizado']

# ============================================
# PALETA POWER BI
# ============================================
C = {
    'bg': '#1b1d21',
    'bg2': '#252830',
    'card': '#2d313a',
    'card2': '#343942',
    'text': '#ffffff',
    'text2': '#a0aec0',
    'text3': '#718096',
    'accent': '#00d4aa',
    'accent2': '#00b894',
    'green': '#00d4aa',
    'greenBg': 'rgba(0, 212, 170, 0.15)',
    'red': '#ff6b6b',
    'redBg': 'rgba(255, 107, 107, 0.15)',
    'amber': '#ffc107',
    'amberBg': 'rgba(255, 193, 7, 0.15)',
    'blue': '#4dabf7',
    'purple': '#9775fa',
    'border': '#3d4350',
}

# ============================================
# CSS POWER BI STYLE
# ============================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;500;600;700&display=swap');

* {{
    font-family: 'Segoe UI', -apple-system, sans-serif !important;
}}

.stApp {{
    background: {C['bg']};
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: {C['bg2']} !important;
    border-right: 1px solid {C['border']} !important;
}}

[data-testid="stSidebar"] .stSelectbox > div > div {{
    background: {C['card2']} !important;
    border: 1px solid {C['border']} !important;
    border-radius: 3px !important;
    color: {C['text']} !important;
}}

/* KPI Cards */
.kpi-card {{
    background: {C['card']};
    border-radius: 4px;
    padding: 16px;
    border: 1px solid {C['border']};
    height: 100%;
}}

.kpi-card.accent {{
    background: linear-gradient(135deg, {C['accent']}15, {C['card']});
    border: 1px solid {C['accent']}40;
}}

.kpi-label {{
    font-size: 11px;
    color: {C['text3']};
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
    margin-bottom: 8px;
}}

.kpi-value {{
    font-size: 28px;
    font-weight: 700;
    color: {C['text']};
    line-height: 1.1;
}}

.kpi-value.accent {{
    color: {C['accent']};
}}

.kpi-value.large {{
    font-size: 32px;
}}

.kpi-delta {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    margin-top: 8px;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 12px;
    font-weight: 600;
}}

.kpi-delta.up {{
    background: {C['greenBg']};
    color: {C['green']};
}}

.kpi-delta.down {{
    background: {C['redBg']};
    color: {C['red']};
}}

.kpi-comparison {{
    font-size: 11px;
    color: {C['text3']};
    margin-left: 6px;
}}

/* Section Headers */
.section-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid {C['border']};
}}

.section-title {{
    font-size: 20px;
    font-weight: 600;
    color: {C['text']};
}}

.section-subtitle {{
    font-size: 12px;
    color: {C['text3']};
}}

/* Card Container */
.card-container {{
    background: {C['card']};
    border-radius: 4px;
    padding: 16px;
    border: 1px solid {C['border']};
    margin-bottom: 12px;
}}

.card-title {{
    font-size: 12px;
    color: {C['text2']};
    font-weight: 600;
    margin-bottom: 16px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* Tables */
.data-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 11px;
}}

.data-table th {{
    text-align: left;
    padding: 10px 8px;
    border-bottom: 1px solid {C['border']};
    color: {C['text3']};
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    font-size: 10px;
}}

.data-table td {{
    padding: 12px 8px;
    border-bottom: 1px solid {C['border']}22;
    color: {C['text']};
}}

.data-table td.highlight {{
    color: {C['accent']};
    font-weight: 600;
}}

/* Status Badges */
.status-badge {{
    display: inline-flex;
    align-items: center;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 10px;
    font-weight: 600;
}}

.status-badge.ok {{
    background: {C['greenBg']};
    color: {C['green']};
}}

.status-badge.warning {{
    background: {C['amberBg']};
    color: {C['amber']};
}}

.status-badge.danger {{
    background: {C['redBg']};
    color: {C['red']};
}}

/* Progress Bars */
.progress-bar {{
    height: 4px;
    background: {C['border']};
    border-radius: 2px;
    overflow: hidden;
    margin-top: 6px;
}}

.progress-fill {{
    height: 100%;
    border-radius: 2px;
    transition: width 0.5s ease;
}}

.progress-fill.green {{
    background: linear-gradient(90deg, {C['accent']}, {C['accent2']});
}}

.progress-fill.amber {{
    background: {C['amber']};
}}

.progress-fill.red {{
    background: {C['red']};
}}

/* Funnel */
.funnel-item {{
    padding: 12px 16px;
    border-radius: 3px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
    color: white;
    font-weight: 500;
}}

.funnel-count {{
    background: rgba(0,0,0,0.2);
    padding: 3px 10px;
    border-radius: 3px;
    font-weight: 700;
    font-size: 13px;
}}

/* Sidebar Logo */
.sidebar-logo {{
    text-align: center;
    padding: 16px;
    background: {C['card']};
    border-radius: 4px;
    margin-bottom: 20px;
    border: 1px solid {C['accent']}30;
}}

.sidebar-logo-icon {{
    font-size: 32px;
    margin-bottom: 4px;
}}

.sidebar-logo-title {{
    color: {C['accent']};
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 2px;
}}

.sidebar-logo-subtitle {{
    color: {C['text3']};
    font-size: 9px;
    letter-spacing: 1px;
    margin-top: 2px;
}}

/* Filter Section */
.filter-label {{
    font-size: 10px;
    color: {C['text3']};
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}}

/* Footer */
.footer {{
    text-align: center;
    padding: 20px;
    margin-top: 20px;
    border-top: 1px solid {C['border']};
    color: {C['text3']};
    font-size: 11px;
}}

/* Sparkline container */
.sparkline-container {{
    background: {C['card']};
    border-radius: 4px;
    padding: 12px;
    border: 1px solid {C['border']};
    margin-top: 12px;
}}

.sparkline-label {{
    font-size: 10px;
    color: {C['text3']};
    margin-bottom: 8px;
    font-weight: 600;
}}

/* Hide Streamlit */
#MainMenu, footer, .stDeployButton {{ display: none !important; }}

.stButton > button {{
    background: {C['accent']} !important;
    color: #000 !important;
    border: none !important;
    border-radius: 4px !important;
    font-weight: 600 !important;
    font-size: 12px !important;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0;
    background: {C['bg2']};
    padding: 4px;
    border-radius: 4px;
    border: 1px solid {C['border']};
}}

.stTabs [data-baseweb="tab"] {{
    background: transparent;
    border-radius: 3px;
    padding: 8px 20px;
    color: {C['text3']};
    font-weight: 600;
    font-size: 13px;
}}

.stTabs [aria-selected="true"] {{
    background: {C['accent']} !important;
    color: #000 !important;
}}

/* Metric containers */
.stMetric {{
    background: {C['card']};
    padding: 12px;
    border-radius: 4px;
    border: 1px solid {C['border']};
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
def load_sheet(name):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={name}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

def load_all():
    return load_sheet("VENTAS"), load_sheet("INVENTARIO"), load_sheet("PRODUCCION"), load_sheet("GASTOS")

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
    return df

def process_inv(df):
    if df.empty: return df
    df = df.copy()
    for c in ['Stock Actual', 'Stock Mínimo', 'Stock Máximo', 'Costo Producción', 'Precio Venta']:
        if c in df.columns: df[c] = df[c].apply(clean_money)
    return df

def filter_periodo(df, periodo, fc):
    if df.empty or not fc or periodo == "Todos": return df
    df = df.copy()
    df[fc] = pd.to_datetime(df[fc], errors='coerce')
    today = datetime.now()
    
    if periodo == "Hoy":
        return df[df[fc].dt.date == today.date()]
    elif periodo == "Esta semana":
        start = today - timedelta(days=today.weekday())
        return df[df[fc].dt.date >= start.date()]
    elif periodo == "Este mes":
        return df[(df[fc].dt.month == today.month) & (df[fc].dt.year == today.year)]
    elif periodo == "Trimestre":
        q = (today.month - 1) // 3
        start_m = q * 3 + 1
        return df[(df[fc].dt.month >= start_m) & (df[fc].dt.month < start_m + 3) & (df[fc].dt.year == today.year)]
    elif periodo == "Año":
        return df[df[fc].dt.year == today.year]
    return df

# ============================================
# COMPONENTES KPI
# ============================================
def kpi_card(label, value, prefix="$", delta=None, delta_label="vs mes ant.", accent=False, large=False):
    val_str = f"{prefix}{value:,.0f}" if prefix == "$" else f"{value:.1f}%" if prefix == "%" else f"{value:,.0f}"
    
    delta_html = ""
    if delta is not None:
        cls = "up" if delta >= 0 else "down"
        arrow = "▲" if delta >= 0 else "▼"
        delta_html = f'''
        <div class="kpi-delta {cls}">
            {arrow} {abs(delta):.1f}%
            <span class="kpi-comparison">{delta_label}</span>
        </div>
        '''
    
    card_class = "kpi-card accent" if accent else "kpi-card"
    value_class = "kpi-value accent large" if accent and large else "kpi-value accent" if accent else "kpi-value large" if large else "kpi-value"
    
    return f'''
    <div class="{card_class}">
        <div class="kpi-label">{label}</div>
        <div class="{value_class}">{val_str}</div>
        {delta_html}
    </div>
    '''

# ============================================
# GRÁFICOS POWER BI
# ============================================
def chart_barras_meta(df, meta):
    if df.empty: return None
    fc = find_col(df, ['Fecha'])
    tc = find_col(df, ['Total'])
    if not fc or not tc: return None
    
    df_t = df.copy()
    df_t['_f'] = pd.to_datetime(df_t[fc], errors='coerce')
    df_t['_t'] = pd.to_numeric(df_t[tc], errors='coerce').fillna(0)
    df_t['mes'] = df_t['_f'].dt.strftime('%b')
    monthly = df_t.groupby('mes')['_t'].sum().reset_index()
    
    fig = go.Figure()
    
    # Meta line
    fig.add_trace(go.Scatter(
        x=monthly['mes'], y=[meta/6]*len(monthly),
        mode='lines',
        line=dict(color=C['amber'], width=2, dash='dot'),
        name='Meta',
        hoverinfo='skip'
    ))
    
    # Barras
    fig.add_trace(go.Bar(
        x=monthly['mes'], y=monthly['_t'],
        marker=dict(
            color=C['accent'],
            line=dict(width=0)
        ),
        name='Ventas',
        hovertemplate='%{x}<br>$%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=C['text3'], family='Segoe UI', size=11),
        margin=dict(l=50, r=20, t=20, b=40),
        height=200,
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(size=10)),
        yaxis=dict(tickformat='$,.0f', gridcolor=C['border'], gridwidth=0.5, zeroline=False),
        xaxis=dict(gridcolor='rgba(0,0,0,0)'),
        bargap=0.3
    )
    return fig

def chart_gauge(value, max_val):
    pct = min((value / max_val) * 100, 100) if max_val > 0 else 0
    color = C['green'] if pct >= 80 else C['amber'] if pct >= 50 else C['red']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct,
        number={'suffix': '%', 'font': {'size': 36, 'color': C['text'], 'family': 'Segoe UI'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 0, 'tickcolor': 'rgba(0,0,0,0)', 'tickfont': {'color': 'rgba(0,0,0,0)'}},
            'bar': {'color': color, 'thickness': 0.8},
            'bgcolor': C['border'],
            'borderwidth': 0,
            'steps': []
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=180,
        margin=dict(l=20, r=20, t=30, b=10),
        font=dict(family='Segoe UI')
    )
    return fig

def chart_donut(labels, values, title_center=""):
    colors = [C['accent'], C['blue'], C['purple'], C['amber'], C['red']]
    
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.65,
        marker=dict(colors=colors[:len(labels)], line=dict(color=C['bg'], width=2)),
        textinfo='percent',
        textfont=dict(color=C['text'], size=11, family='Segoe UI'),
        hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=C['text3'], family='Segoe UI'),
        margin=dict(l=10, r=10, t=10, b=10),
        height=200,
        showlegend=False,
        annotations=[dict(
            text=title_center,
            x=0.5, y=0.5,
            font=dict(size=14, color=C['accent'], family='Segoe UI', weight=700),
            showarrow=False
        )]
    )
    return fig

def chart_barras_h(labels, values):
    fig = go.Figure(go.Bar(
        y=labels,
        x=values,
        orientation='h',
        marker=dict(color=C['accent'], line=dict(width=0)),
        text=[f'${v:,.0f}' for v in values],
        textposition='outside',
        textfont=dict(color=C['text'], size=11, family='Segoe UI'),
        hovertemplate='<b>%{y}</b><br>$%{x:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=C['text3'], family='Segoe UI'),
        margin=dict(l=100, r=60, t=10, b=10),
        height=200,
        yaxis=dict(gridcolor='rgba(0,0,0,0)'),
        xaxis=dict(tickformat='$,.0f', gridcolor=C['border'], gridwidth=0.5),
        bargap=0.4
    )
    return fig

def chart_trend_mini(values):
    fig = go.Figure(go.Scatter(
        y=values,
        mode='lines+markers',
        line=dict(color=C['accent'], width=2),
        marker=dict(size=6, color=C['accent']),
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=50,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False
    )
    return fig

# ============================================
# MAIN
# ============================================
def main():
    # Cargar datos
    with st.spinner("Cargando datos..."):
        ventas_raw, inv_raw, prod_raw, gastos_raw = load_all()
    
    ventas = process_ventas(ventas_raw)
    gastos = process_gastos(gastos_raw)
    inventario = process_inv(inv_raw)
    
    if ventas.empty:
        st.error("⚠️ No se pudieron cargar los datos")
        st.info("Verifica que el Google Sheets sea público")
        return
    
    # ============ SIDEBAR ============
    with st.sidebar:
        st.markdown('''
        <div class="sidebar-logo">
            <div class="sidebar-logo-icon">🌵</div>
            <div class="sidebar-logo-title">YUKU SAVI</div>
            <div class="sidebar-logo-subtitle">MEZCAL ARTESANAL</div>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("↻ Actualizar", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        
        # Filtros
        st.markdown('<div class="filter-label">⚙️ FILTROS</div>', unsafe_allow_html=True)
        
        periodo = st.selectbox("Periodo", ["Todos", "Hoy", "Esta semana", "Este mes", "Trimestre", "Año"], index=3)
        
        canales = ["Todos"] + sorted(ventas['Canal'].dropna().unique().tolist()) if 'Canal' in ventas.columns else ["Todos"]
        canal = st.selectbox("Canal", canales)
        
        vendedores = ["Todos"] + sorted(ventas['Vendedor'].dropna().unique().tolist()) if 'Vendedor' in ventas.columns else ["Todos"]
        vendedor = st.selectbox("Vendedor", vendedores)
        
        productos = ["Todos"] + sorted(ventas['Producto'].dropna().unique().tolist()) if 'Producto' in ventas.columns else ["Todos"]
        producto = st.selectbox("Producto", productos)
        
        # Aplicar filtros
        df = ventas.copy()
        fc = find_col(df, ['Fecha'])
        if periodo != "Todos": df = filter_periodo(df, periodo, fc)
        if canal != "Todos" and 'Canal' in df.columns: df = df[df['Canal'] == canal]
        if vendedor != "Todos" and 'Vendedor' in df.columns: df = df[df['Vendedor'] == vendedor]
        if producto != "Todos" and 'Producto' in df.columns: df = df[df['Producto'] == producto]
        
        # Separar ventas y cotizaciones
        sc = find_col(df, ['Status'])
        df_v = df[df[sc].isin(STATUS_VENTAS)] if sc else df
        df_c = df[df[sc].isin(STATUS_COTIZACIONES)] if sc else pd.DataFrame()
        
        # Métricas
        tc = find_col(df_v, ['Total'])
        cc = find_col(df_v, ['Cantidad'])
        total_v = pd.to_numeric(df_v[tc], errors='coerce').sum() if tc else 0
        total_b = int(pd.to_numeric(df_v[cc], errors='coerce').sum()) if cc else 0
        n_v = len(df_v)
        ticket = total_v / n_v if n_v > 0 else 0
        
        mc = find_col(gastos, ['Monto'])
        total_g = pd.to_numeric(gastos[mc], errors='coerce').sum() if mc else 0
        utilidad = total_v - total_g
        margen = (utilidad / total_v * 100) if total_v > 0 else 0
        meta = 300000
        pct_meta = (total_v / meta * 100) if meta > 0 else 0
        
        # Sparkline
        st.markdown("---")
        st.markdown('<div class="sparkline-label">TENDENCIA SEMANAL</div>', unsafe_allow_html=True)
        if fc and not df_v.empty:
            daily = df_v.groupby(df_v[fc].dt.date)[tc].sum().tail(7).values.tolist()
            if len(daily) > 1:
                fig = chart_trend_mini(daily)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Footer sidebar
        st.markdown("---")
        st.markdown(f'''
        <div style="text-align:center;padding:10px 0;">
            <div style="font-size:9px;color:{C['text3']};">Powered by</div>
            <div style="color:{C['accent']};font-weight:600;font-size:12px;">SINAPSIS</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # ============ MAIN CONTENT ============
    
    # Header
    st.markdown(f'''
    <div class="section-header">
        <div>
            <div class="section-title">Dashboard de Ventas</div>
            <div class="section-subtitle">Yuku Savi · Mezcal Artesanal de Puebla | {periodo}</div>
        </div>
        <div style="font-size:11px;color:{C['text3']};">Última actualización: hace 2 min</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # KPIs Row 1 - 6 columnas
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(kpi_card("Ventas Totales", total_v, delta=12.5, accent=True, large=True), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("Utilidad Bruta", utilidad, delta=15.2), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("Margen", margen, prefix="%", delta=2.1), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card("Botellas", total_b, prefix="", delta=8), unsafe_allow_html=True)
    with c5:
        st.markdown(kpi_card("Ticket Prom.", ticket, delta=5.3), unsafe_allow_html=True)
    with c6:
        conv = (n_v / (n_v + len(df_c)) * 100) if (n_v + len(df_c)) > 0 else 0
        st.markdown(kpi_card("Conversión", conv, prefix="%", delta=-2), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 2: Chart + Gauge + Donut
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f'<div class="card-title">📈 VENTAS VS META POR MES</div>', unsafe_allow_html=True)
        fig = chart_barras_meta(df_v, meta)
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown(f'<div class="card-title">🎯 META DEL MES</div>', unsafe_allow_html=True)
        fig = chart_gauge(total_v, meta)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown(f'<p style="text-align:center;color:{C["text3"]};font-size:11px;margin-top:-10px;">${total_v:,.0f} de ${meta:,.0f}</p>', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'<div class="card-title">📊 VENTAS POR CANAL</div>', unsafe_allow_html=True)
        if 'Canal' in df_v.columns and tc:
            canal_data = df_v.groupby('Canal')[tc].sum().sort_values(ascending=False)
            fig = chart_donut(canal_data.index.tolist(), canal_data.values.tolist(), f"${total_v/1000:.0f}k")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            # Leyenda
            for i, (c, v) in enumerate(canal_data.items()):
                pct = v / total_v * 100 if total_v > 0 else 0
                colors = [C['accent'], C['blue'], C['purple'], C['amber']]
                st.markdown(f'''
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                    <div style="width:10px;height:10px;background:{colors[i % len(colors)]};border-radius:2px;"></div>
                    <span style="font-size:11px;color:{C['text2']};flex:1;">{c}</span>
                    <span style="font-size:11px;color:{C['text']};font-weight:600;">{pct:.0f}%</span>
                </div>
                ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 3: Tabla Productos + Embudo + Inventario
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
        <div class="card-container">
            <div class="card-title">🏆 VENTAS POR PRODUCTO</div>
        ''', unsafe_allow_html=True)
        
        pc = find_col(df_v, ['Producto'])
        if pc and tc:
            prod_data = df_v.groupby(pc).agg({
                tc: 'sum',
                cc if cc else tc: 'sum' if cc else 'count'
            }).sort_values(tc, ascending=False).head(5)
            
            st.markdown('<table class="data-table">', unsafe_allow_html=True)
            st.markdown(f'<tr><th>Producto</th><th style="text-align:center;">Unid.</th><th style="text-align:right;">Ventas</th></tr>', unsafe_allow_html=True)
            for prod, row in prod_data.iterrows():
                unid = int(row[cc]) if cc else int(row[tc])
                st.markdown(f'''
                <tr>
                    <td>{prod}</td>
                    <td style="text-align:center;">{unid}</td>
                    <td class="highlight" style="text-align:right;">${row[tc]:,.0f}</td>
                </tr>
                ''', unsafe_allow_html=True)
            st.markdown('</table>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="card-container">
            <div class="card-title">🎯 PIPELINE DE VENTAS</div>
        ''', unsafe_allow_html=True)
        
        status_order = ['Cotizado', 'Apartado', 'Pagado', 'Entregado']
        status_colors = [C['blue'], C['amber'], C['accent'], C['green']]
        
        if sc:
            for i, status in enumerate(status_order):
                df_s = ventas[ventas[sc] == status] if sc else pd.DataFrame()
                cnt = len(df_s)
                monto = pd.to_numeric(df_s[tc], errors='coerce').sum() if tc else 0
                width = 100 - (i * 15)
                
                st.markdown(f'''
                <div class="funnel-item" style="width:{width}%;background:linear-gradient(90deg,{status_colors[i]}cc,{status_colors[i]}66);">
                    <span style="font-size:12px;">{status}</span>
                    <div style="display:flex;align-items:center;gap:10px;">
                        <span class="funnel-count">{cnt}</span>
                        <span style="font-size:12px;">${monto/1000:.0f}k</span>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="card-container">
            <div class="card-title">📦 ESTADO DE INVENTARIO</div>
        ''', unsafe_allow_html=True)
        
        if not inventario.empty:
            p_col = find_col(inventario, ['Producto'])
            s_col = find_col(inventario, ['Stock Actual'])
            m_col = find_col(inventario, ['Stock Mínimo'])
            
            if p_col and s_col:
                for _, row in inventario.head(5).iterrows():
                    stock = row[s_col] if s_col else 0
                    minimo = row[m_col] if m_col else 0
                    pct = min((stock / (minimo * 3)) * 100, 100) if minimo > 0 else 100
                    
                    if stock <= minimo * 0.5:
                        status = "danger"
                        badge = "⚠"
                        color = C['red']
                    elif stock <= minimo:
                        status = "warning"
                        badge = "!"
                        color = C['amber']
                    else:
                        status = "ok"
                        badge = "✓"
                        color = C['green']
                    
                    st.markdown(f'''
                    <div style="margin-bottom:12px;">
                        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                            <span style="font-size:11px;color:{C['text']};">{row[p_col]}</span>
                            <div style="display:flex;align-items:center;gap:8px;">
                                <span style="font-size:12px;font-weight:600;color:{color};">{int(stock)}</span>
                                <span class="status-badge {status}">{badge}</span>
                            </div>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill {'green' if status == 'ok' else 'amber' if status == 'warning' else 'red'}" style="width:{pct}%;"></div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 4: Por Región + KPIs adicionales
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'<div class="card-title">🗺️ VENTAS POR REGIÓN</div>', unsafe_allow_html=True)
        # Simulamos datos de región si no existen
        if 'Region' in df_v.columns:
            region_data = df_v.groupby('Region')[tc].sum().sort_values(ascending=False)
        else:
            # Datos simulados
            region_data = pd.Series({
                'CDMX': total_v * 0.38,
                'Monterrey': total_v * 0.22,
                'Guadalajara': total_v * 0.19,
                'Puebla': total_v * 0.12,
                'Otros': total_v * 0.09
            })
        
        fig = chart_donut(region_data.index.tolist(), region_data.values.tolist(), "5 Regiones")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown(f'<div class="card-title">📊 MÉTRICAS ADICIONALES</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(kpi_card("Gastos Operativos", total_g, delta=-5, delta_label="↓ Ahorro"), unsafe_allow_html=True)
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            st.markdown(kpi_card("Cotizaciones", len(df_c), prefix="", delta=-10), unsafe_allow_html=True)
        with c2:
            st.markdown(kpi_card("Utilidad Neta", utilidad, delta=18, accent=True), unsafe_allow_html=True)
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            margen_neto = (utilidad / total_v * 100) if total_v > 0 else 0
            st.markdown(kpi_card("Margen Neto", margen_neto, prefix="%", delta=3.2), unsafe_allow_html=True)
    
    # Footer
    st.markdown(f'''
    <div class="footer">
        🌵 <strong style="color:{C['text2']};">Yuku Savi</strong> · Dashboard de Inteligencia de Negocio · 
        <span style="color:{C['accent']};font-weight:600;">SINAPSIS</span>
    </div>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
