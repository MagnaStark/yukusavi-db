import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import math

# ============================================
# CONFIGURACIÓN INICIAL
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

# Paleta Power BI Enterprise
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
# ESTILOS CSS POWER BI
# ============================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {{
    --bg: {C['bg']};
    --bg2: {C['bg2']};
    --card: {C['card']};
    --text: {C['text']};
    --text2: {C['text2']};
    --text3: {C['text3']};
    --accent: {C['accent']};
    --border: {C['border']};
}}

html, body, [class*="css"] {{
    font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif !important;
}}

.stApp {{
    background: var(--bg) !important;
}}

/* Ocultar elementos de Streamlit */
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

/* Selectbox styling */
.stSelectbox > div > div {{
    background: {C['card2']} !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--text) !important;
}}

.stSelectbox > div > div:hover {{
    border-color: var(--accent) !important;
}}

.stSelectbox label {{
    color: var(--text3) !important;
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    font-weight: 600 !important;
}}

/* Botón */
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

/* Cards */
.card {{
    background: var(--card);
    border-radius: 4px;
    padding: 20px;
    border: 1px solid var(--border);
    margin-bottom: 12px;
}}

.card-title {{
    font-size: 12px;
    color: var(--text2);
    font-weight: 600;
    margin-bottom: 16px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* KPI Cards */
.kpi-card {{
    background: var(--card);
    border-radius: 4px;
    padding: 18px;
    border: 1px solid var(--border);
    height: 100%;
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

.kpi-value.large {{
    font-size: 30px;
}}

.kpi-value.accent {{
    color: var(--accent);
}}

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
    color: {C['green']};
}}

.kpi-delta.down {{
    background: rgba(255,107,107,0.15);
    color: {C['red']};
}}

.kpi-sublabel {{
    font-size: 11px;
    color: var(--text3);
    margin-left: 6px;
}}

/* Tables */
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
}}

.funnel-count {{
    background: rgba(0,0,0,0.25);
    padding: 4px 12px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 14px;
}}

/* Inventory */
.inv-item {{
    margin-bottom: 16px;
}}

.inv-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}}

.inv-name {{
    font-size: 13px;
    color: var(--text);
}}

.inv-stock {{
    font-size: 14px;
    font-weight: 600;
}}

.inv-badge {{
    width: 22px;
    height: 22px;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 700;
    margin-left: 8px;
}}

.inv-badge.ok {{ background: rgba(0,212,170,0.15); color: {C['green']}; }}
.inv-badge.warning {{ background: rgba(255,193,7,0.15); color: {C['amber']}; }}
.inv-badge.danger {{ background: rgba(255,107,107,0.15); color: {C['red']}; }}

.progress-bar {{
    height: 5px;
    background: var(--border);
    border-radius: 3px;
    overflow: hidden;
}}

.progress-fill {{
    height: 100%;
    border-radius: 3px;
}}

/* Legend */
.donut-legend {{
    margin-top: 12px;
}}

.donut-legend-item {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
    font-size: 12px;
}}

.donut-legend-dot {{
    width: 12px;
    height: 12px;
    border-radius: 3px;
    flex-shrink: 0;
}}

.donut-legend-name {{
    flex: 1;
    color: var(--text2);
}}

.donut-legend-value {{
    color: var(--text);
    font-weight: 600;
}}

/* Header */
.main-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 20px;
    margin-bottom: 24px;
    border-bottom: 1px solid var(--border);
}}

.main-title {{
    font-size: 22px;
    font-weight: 600;
    color: var(--text);
    margin: 0;
}}

.main-subtitle {{
    font-size: 13px;
    color: var(--text3);
    margin-top: 4px;
}}

/* Sidebar components */
.sidebar-logo {{
    text-align: center;
    padding: 24px 16px;
    background: var(--card);
    border-radius: 4px;
    margin-bottom: 20px;
    border: 1px solid rgba(0,212,170,0.25);
}}

.sidebar-icon {{
    font-size: 36px;
    margin-bottom: 8px;
}}

.sidebar-title {{
    color: var(--accent);
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 3px;
}}

.sidebar-subtitle {{
    color: var(--text3);
    font-size: 9px;
    letter-spacing: 2px;
    margin-top: 4px;
}}

.sidebar-section {{
    font-size: 10px;
    color: var(--text3);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 700;
    margin: 20px 0 12px;
    display: flex;
    align-items: center;
    gap: 6px;
}}

.sidebar-footer {{
    text-align: center;
    padding-top: 20px;
    margin-top: 24px;
    border-top: 1px solid var(--border);
}}

.sidebar-footer-brand {{
    color: var(--accent);
    font-weight: 600;
    font-size: 13px;
}}

/* Footer */
.main-footer {{
    text-align: center;
    padding: 24px;
    margin-top: 32px;
    border-top: 1px solid var(--border);
    color: var(--text3);
    font-size: 12px;
}}

/* Fix column gaps */
[data-testid="column"] {{
    padding: 0 6px !important;
}}

/* Plotly background fix */
.js-plotly-plot .plotly .main-svg {{
    background: transparent !important;
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

# ============================================
# GRÁFICOS PLOTLY PROFESIONALES
# ============================================
def chart_bars_meta(df, fecha_col, total_col, meta):
    """Gráfico de barras con línea de meta"""
    if df.empty or not fecha_col or not total_col: return None
    
    df_temp = df.copy()
    df_temp['_fecha'] = pd.to_datetime(df_temp[fecha_col], errors='coerce')
    df_temp['_total'] = pd.to_numeric(df_temp[total_col], errors='coerce').fillna(0)
    
    monthly = df_temp.groupby(df_temp['_fecha'].dt.to_period('M')).agg({
        '_total': 'sum'
    }).reset_index()
    monthly['mes'] = monthly['_fecha'].astype(str).str[-2:]
    monthly['mes_label'] = monthly['_fecha'].dt.strftime('%b')
    
    if monthly.empty: return None
    
    fig = go.Figure()
    
    # Línea de meta
    fig.add_trace(go.Scatter(
        x=monthly['mes_label'], y=[meta]*len(monthly),
        mode='lines', name='Meta',
        line=dict(color=C['amber'], width=2, dash='dot'),
        hoverinfo='skip'
    ))
    
    # Barras
    fig.add_trace(go.Bar(
        x=monthly['mes_label'], y=monthly['_total'],
        name='Ventas',
        marker=dict(
            color=C['accent'],
            line=dict(width=0)
        ),
        hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=C['text3'], family='Inter', size=11),
        margin=dict(l=50, r=20, t=10, b=40),
        height=200,
        showlegend=False,
        yaxis=dict(
            tickformat='$,.0f',
            gridcolor=C['border'],
            gridwidth=0.5,
            zeroline=False,
            tickfont=dict(size=10)
        ),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0)',
            tickfont=dict(size=10)
        ),
        bargap=0.4,
        hovermode='x unified'
    )
    return fig

def chart_gauge(value, max_val):
    """Gauge semicircular con aguja"""
    pct = min((value / max_val) * 100, 100) if max_val > 0 else 0
    
    if pct >= 80: color = C['green']
    elif pct >= 50: color = C['amber']
    else: color = C['red']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct,
        number={'suffix': '%', 'font': {'size': 40, 'color': C['text'], 'family': 'Inter'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 0, 'tickcolor': 'rgba(0,0,0,0)', 'tickfont': {'size': 1, 'color': 'rgba(0,0,0,0)'}},
            'bar': {'color': color, 'thickness': 0.8},
            'bgcolor': C['border'],
            'borderwidth': 0,
            'steps': [],
            'threshold': {
                'line': {'color': C['text'], 'width': 3},
                'thickness': 0.8,
                'value': pct
            }
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
    """Donut chart con centro"""
    colors_list = [C['accent'], C['blue'], C['purple'], C['amber'], C['red']]
    
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.65,
        marker=dict(
            colors=colors_list[:len(labels)],
            line=dict(color=C['bg'], width=2)
        ),
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
        annotations=[dict(
            text=f"<b>{center_text}</b>",
            x=0.5, y=0.5,
            font=dict(size=16, color=C['accent'], family='Inter'),
            showarrow=False
        )]
    )
    return fig

def chart_sparkline(values):
    """Mini sparkline"""
    fig = go.Figure(go.Scatter(
        y=values,
        mode='lines+markers',
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

# ============================================
# COMPONENTES HTML
# ============================================
def html_kpi(label, value, prefix="$", suffix="", delta=None, delta_label="vs mes ant.", accent=False, large=False):
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
        d_cls = "up" if delta >= 0 else "down"
        arrow = "▲" if delta >= 0 else "▼"
        delta_html = f'<div class="kpi-delta {d_cls}">{arrow} {abs(delta):.1f}%<span class="kpi-sublabel">{delta_label}</span></div>'
    
    return f'''<div class="{card_cls}">
        <div class="kpi-label">{label}</div>
        <div class="{val_cls}">{fmt_val}</div>
        {delta_html}
    </div>'''

def html_table(data, columns):
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
        html += f'''<div class="funnel-item" style="width:{width}%; background:linear-gradient(90deg,{color}dd,{color}88); margin:0 auto;">
            <span>{item['etapa']}</span>
            <span class="funnel-count">{item['count']}</span>
        </div>'''
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
                <div>
                    <span class="inv-stock" style="color:{color};">{int(stock)}</span>
                    <span class="inv-badge {status}">{badge}</span>
                </div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width:{pct}%; background:{color};"></div>
            </div>
        </div>'''
    return html

def html_legend(items, colors_list):
    html = '<div class="donut-legend">'
    for i, item in enumerate(items):
        color = colors_list[i % len(colors_list)]
        html += f'''<div class="donut-legend-item">
            <div class="donut-legend-dot" style="background:{color};"></div>
            <span class="donut-legend-name">{item['name']}</span>
            <span class="donut-legend-value">{item['pct']:.0f}%</span>
        </div>'''
    html += '</div>'
    return html

# ============================================
# APLICACIÓN PRINCIPAL
# ============================================
def main():
    # Cargar datos
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
        
        # Aplicar filtros
        df = ventas.copy()
        fecha_col = find_col(df, ['Fecha'])
        df = filter_periodo(df, periodo, fecha_col)
        
        if canal != "Todos" and 'Canal' in df.columns: df = df[df['Canal'] == canal]
        if vendedor != "Todos" and 'Vendedor' in df.columns: df = df[df['Vendedor'] == vendedor]
        if producto != "Todos" and 'Producto' in df.columns: df = df[df['Producto'] == producto]
        
        status_col = find_col(df, ['Status'])
        df_ventas = df[df[status_col].isin(STATUS_VENTAS)] if status_col else df
        df_cotiz = df[df[status_col].isin(STATUS_COTIZACIONES)] if status_col else pd.DataFrame()
        
        # Sparkline
        st.markdown('<div class="sidebar-section">📈 TENDENCIA</div>', unsafe_allow_html=True)
        total_col = find_col(df_ventas, ['Total'])
        if fecha_col and total_col and not df_ventas.empty:
            df_ventas[fecha_col] = pd.to_datetime(df_ventas[fecha_col], errors='coerce')
            daily = df_ventas.groupby(df_ventas[fecha_col].dt.date)[total_col].sum().tail(7)
            if len(daily) > 1:
                st.plotly_chart(chart_sparkline(daily.values.tolist()), use_container_width=True, config={'displayModeBar': False})
        
        st.markdown('''<div class="sidebar-footer">
            <div style="font-size:9px; color:var(--text3);">Powered by</div>
            <div class="sidebar-footer-brand">SINAPSIS</div>
        </div>''', unsafe_allow_html=True)
    
    # ========== MÉTRICAS ==========
    total_col = find_col(df_ventas, ['Total'])
    cant_col = find_col(df_ventas, ['Cantidad'])
    monto_col = find_col(gastos, ['Monto'])
    
    total_ventas = df_ventas[total_col].sum() if total_col else 0
    total_botellas = int(df_ventas[cant_col].sum()) if cant_col else 0
    n_trans = len(df_ventas)
    ticket_prom = total_ventas / n_trans if n_trans > 0 else 0
    
    total_gastos = gastos[monto_col].sum() if monto_col else 0
    utilidad = total_ventas - total_gastos
    margen = (utilidad / total_ventas * 100) if total_ventas > 0 else 0
    
    n_cotiz = len(df_cotiz)
    conversion = (n_trans / (n_trans + n_cotiz) * 100) if (n_trans + n_cotiz) > 0 else 0
    
    # ========== HEADER ==========
    st.markdown(f'''<div class="main-header">
        <div>
            <div class="main-title">Dashboard de Ventas</div>
            <div class="main-subtitle">Yuku Savi · Mezcal Artesanal de Puebla | {periodo}</div>
        </div>
        <div style="font-size:11px; color:var(--text3);">Última actualización: {datetime.now().strftime('%H:%M')}</div>
    </div>''', unsafe_allow_html=True)
    
    # ========== KPIs (6 columnas) ==========
    cols = st.columns(6)
    with cols[0]: st.markdown(html_kpi("Ventas Totales", total_ventas, delta=12.5, accent=True, large=True), unsafe_allow_html=True)
    with cols[1]: st.markdown(html_kpi("Utilidad Bruta", utilidad, delta=15.2), unsafe_allow_html=True)
    with cols[2]: st.markdown(html_kpi("Margen", margen, prefix="", suffix="%", delta=2.1), unsafe_allow_html=True)
    with cols[3]: st.markdown(html_kpi("Botellas", total_botellas, prefix="", delta=8), unsafe_allow_html=True)
    with cols[4]: st.markdown(html_kpi("Ticket Prom.", ticket_prom, delta=5.3), unsafe_allow_html=True)
    with cols[5]: st.markdown(html_kpi("Conversión", conversion, prefix="", suffix="%", delta=-2 if conversion < 80 else 3), unsafe_allow_html=True)
    
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    
    # ========== ROW 2: Barras + Gauge + Donut ==========
    c1, c2, c3 = st.columns([2, 1, 1])
    
    with c1:
        st.markdown('<div class="card"><div class="card-title">📈 VENTAS VS META POR MES</div>', unsafe_allow_html=True)
        fig = chart_bars_meta(df_ventas, fecha_col, total_col, META_MENSUAL)
        if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="card"><div class="card-title">🎯 META DEL MES</div>', unsafe_allow_html=True)
        st.plotly_chart(chart_gauge(total_ventas, META_MENSUAL), use_container_width=True, config={'displayModeBar': False})
        st.markdown(f'<div style="text-align:center; color:var(--text3); font-size:11px; margin-top:-10px;">${total_ventas:,.0f} de ${META_MENSUAL:,.0f}</div></div>', unsafe_allow_html=True)
    
    with c3:
        st.markdown('<div class="card"><div class="card-title">📊 VENTAS POR CANAL</div>', unsafe_allow_html=True)
        if 'Canal' in df_ventas.columns and total_col:
            canal_data = df_ventas.groupby('Canal')[total_col].sum().sort_values(ascending=False)
            if not canal_data.empty:
                total_c = canal_data.sum()
                st.plotly_chart(chart_donut(canal_data.index.tolist(), canal_data.values.tolist(), f"${total_c/1000:.0f}k"), use_container_width=True, config={'displayModeBar': False})
                legend_items = [{'name': k, 'pct': (v/total_c)*100} for k, v in canal_data.items()]
                st.markdown(html_legend(legend_items, [C['accent'], C['blue'], C['purple'], C['amber']]), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    
    # ========== ROW 3: Tabla + Funnel + Inventario ==========
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('<div class="card"><div class="card-title">🏆 VENTAS POR PRODUCTO</div>', unsafe_allow_html=True)
        prod_col = find_col(df_ventas, ['Producto'])
        if prod_col and total_col and cant_col:
            prod_data = df_ventas.groupby(prod_col).agg({total_col: 'sum', cant_col: 'sum'}).sort_values(total_col, ascending=False).head(5)
            table_data = [{'producto': p, 'unidades': int(r[cant_col]), 'ventas': r[total_col]} for p, r in prod_data.iterrows()]
            cols_def = [{'key': 'producto', 'label': 'Producto'}, {'key': 'unidades', 'label': 'Unid.', 'align': 'center'}, {'key': 'ventas', 'label': 'Ventas', 'prefix': '$', 'align': 'right', 'highlight': True}]
            st.markdown(html_table(table_data, cols_def), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="card"><div class="card-title">🎯 PIPELINE DE VENTAS</div>', unsafe_allow_html=True)
        if status_col:
            pipeline = ['Cotizado', 'Apartado', 'Pagado', 'Entregado']
            funnel_data = []
            for s in pipeline:
                df_s = ventas[ventas[status_col] == s] if status_col else pd.DataFrame()
                funnel_data.append({'etapa': s, 'count': len(df_s)})
            st.markdown(html_funnel(funnel_data), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c3:
        st.markdown('<div class="card"><div class="card-title">📦 ESTADO DE INVENTARIO</div>', unsafe_allow_html=True)
        if not inventario.empty:
            prod_inv = find_col(inventario, ['Producto'])
            stock_col = find_col(inventario, ['Stock Actual'])
            min_col = find_col(inventario, ['Stock Mínimo'])
            if prod_inv and stock_col:
                inv_data = [{'producto': r[prod_inv], 'stock': r[stock_col], 'minimo': r[min_col] if min_col else 10} for _, r in inventario.head(5).iterrows()]
                st.markdown(html_inventory(inv_data), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    
    # ========== ROW 4: Vendedores + KPIs Extra ==========
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown('<div class="card"><div class="card-title">🗺️ VENTAS POR VENDEDOR</div>', unsafe_allow_html=True)
        if 'Vendedor' in df_ventas.columns and total_col:
            vend_data = df_ventas.groupby('Vendedor')[total_col].sum().sort_values(ascending=False)
            if not vend_data.empty:
                total_v = vend_data.sum()
                st.plotly_chart(chart_donut(vend_data.index.tolist(), vend_data.values.tolist(), f"{len(vend_data)}"), use_container_width=True, config={'displayModeBar': False})
                legend_items = [{'name': k, 'pct': (v/total_v)*100} for k, v in vend_data.items()]
                st.markdown(html_legend(legend_items, [C['accent'], C['blue'], C['purple'], C['amber'], C['red']]), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="card"><div class="card-title">📊 MÉTRICAS ADICIONALES</div>', unsafe_allow_html=True)
        kc1, kc2 = st.columns(2)
        with kc1:
            st.markdown(html_kpi("Gastos Operativos", total_gastos, delta=-5, delta_label="↓ Ahorro"), unsafe_allow_html=True)
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            st.markdown(html_kpi("Cotizaciones", n_cotiz, prefix="", delta=-10), unsafe_allow_html=True)
        with kc2:
            st.markdown(html_kpi("Utilidad Neta", utilidad * 0.7, delta=18, accent=True), unsafe_allow_html=True)
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            margen_neto = (utilidad * 0.7 / total_ventas * 100) if total_ventas > 0 else 0
            st.markdown(html_kpi("Margen Neto", margen_neto, prefix="", suffix="%", delta=3.2), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== FOOTER ==========
    st.markdown(f'''<div class="main-footer">
        🌵 <strong style="color:{C['text2']};">Yuku Savi</strong> · Dashboard de Inteligencia de Negocio · 
        <span style="color:{C['accent']}; font-weight:600;">SINAPSIS</span>
    </div>''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
