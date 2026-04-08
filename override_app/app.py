from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import date

from override import (getRatingData, getReasonData, getBolgeData, getOverallData)

app = Flask(__name__)

SEGMENT_LIST = [
    'TÜM MODELLER', '8-40-ÜRETİM', '8-40-HİZMET',
    '40+-ÜRETİM', '40+-HİZMET', '40+-TİCARET', '40+-İNŞAAT'
]

def today():
    return date.today().strftime('%d.%m.%Y')

# ---------------------------------------------------------------------------
# SAYFA ROUTE'LARI
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html', run_date=today())

@app.route('/musteri')
def musteri():
    return render_template('musteri.html', segments=SEGMENT_LIST, run_date=today())

@app.route('/grup')
def grup():
    return render_template('grup.html', segments=SEGMENT_LIST, run_date=today())


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

@app.route('/api/data')
def api_data():
    view  = request.args.get('view',  'musteri')
    tab   = request.args.get('tab',   'Rating')
    model = request.args.get('model', 'TÜM MODELLER')

    musteri_or_grup = 'MUSTERI' if view == 'musteri' else 'GRUP'

    if tab == 'Rating':
        df = getRatingData(musteri_or_grup=musteri_or_grup, model_tipi=model)

        # Kolon isimleri: -5,-4,-3,-2,-1, RATING, RATING_ADET, OVERRIDE_ADET, +0,+1,+2,+3,+4,+5
        neg_cols = ['-5', '-4', '-3', '-2', '-1']
        pos_cols = ['+0', '+1', '+2', '+3', '+4', '+5']
        bar_cols = neg_cols + pos_cols

        # TOTAL satırını ayır
        total_mask = df['RATING'].astype(str).str.upper() == 'TOTAL'
        df_plot    = df[~total_mask].copy()
        df_total   = df[total_mask].copy()
        df_out     = pd.concat([df_plot, df_total], ignore_index=True)

        # OVERRIDE_ORAN zaten SQL'den geliyor, formatlama yapılmıyor (zaten DECIMAL olarak hesaplanmış)

        # ── GRAFİK ──────────────────────────────────────────────
        fig = make_subplots(specs=[[{'secondary_y': True}]])

        # Bar: OVERRIDE_ADET (text olarak OVERRIDE_ORAN göster)
        override_text = (df_plot['OVERRIDE_ORAN'].astype(str) + '%').values
        fig.add_trace(
            go.Bar(
                x=df_plot['RATING'].astype(str),
                y=df_plot['OVERRIDE_ADET'],
                name='Override Adet',
                marker_color='#3b82f6',
                text=override_text,
                textposition='outside',
            ),
            secondary_y=False
        )

        # Line: OVERRIDE_ADET (trend)
        fig.add_trace(
            go.Scatter(
                x=df_plot['RATING'].astype(str),
                y=df_plot['OVERRIDE_ADET'],
                name='Trend',
                mode='lines+markers',
                line=dict(color='red', width=1.5),
                marker=dict(size=5),
            ),
            secondary_y=True
        )

        fig.update_layout(
            title=dict(text='Override Adet Dağılımı', x=0.5,
                       font=dict(size=18, color='#ffffff')),
            template='plotly_white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                        font=dict(color='#94a3b8')),
                        width = 1200,
            margin=dict(t=80, r=20, b=60, l=60),
        )
        fig.update_xaxes(title_text='Rating', type='category',
                         title_font=dict(color='#ffffff'), tickfont=dict(color='#94a3b8'))
        fig.update_yaxes(title_text='Adet', secondary_y=False,
                         title_font=dict(color='#ffffff'), tickfont=dict(color='#94a3b8'))
        fig.update_yaxes(title_text='Trend', secondary_y=True, showgrid=False,
                         title_font=dict(color='#ffffff'), tickfont=dict(color='#94a3b8'))

        # ── TABLO ────────────────────────────────────────────────
        # Gösterilecek kolonlar (OVERRIDE_ORAN da dahil)
        show_cols = neg_cols + ['RATING', 'RATING_ADET', 'OVERRIDE_ADET', 'OVERRIDE_ORAN'] + pos_cols

        # Sadece mevcut kolonları al
        show_cols = [c for c in show_cols if c in df_out.columns]

        table_data    = df_out[show_cols].to_dict(orient='records')
        table_columns = show_cols

        return jsonify({
            'table':   table_data,
            'columns': table_columns,
            'figure':  json.loads(fig.to_json()),
        })

    if tab == 'Reasons':
        import plotly.express as px
        df = getReasonData(musteri_or_grup=musteri_or_grup, model_tipi=model)
        df.columns = [c.strip().replace('"', '') for c in df.columns]
        df = df.rename(columns={'-': 'Negatif', '+': 'Pozitif'})

        total_mask = df['OVERRIDE_REASON'].astype(str).str.upper() == 'TOTAL'
        df_plot    = df[~total_mask].copy()

        fig = px.bar(
            df_plot,
            x='OVERRIDE_REASON',
            y=['Negatif', 'Pozitif'],
            barmode='group',
            color_discrete_map={'Negatif': '#dc2626', 'Pozitif': '#16a34a'},
            text_auto=True,
        )
        fig.update_traces(textfont_size=11, textposition='outside', cliponaxis=False)
        fig.update_layout(
            title=dict(text='Override Reasons', x=0.5, font=dict(size=18, color='#ffffff')),
            width=1200,
            xaxis_title='Override Reason',
            yaxis_title='Adet',
            template='plotly_white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                        font=dict(color='#94a3b8')),
        )
        fig.update_xaxes(title_font=dict(color='#ffffff'), tickfont=dict(color='#94a3b8'))
        fig.update_yaxes(title_font=dict(color='#ffffff'), tickfont=dict(color='#94a3b8'))
        fig.update_xaxes(type='category')

        return jsonify({
            'table':   df.to_dict(orient='records'),
            'columns': list(df.columns),
            'figure':  json.loads(fig.to_json()),
        })

    if tab == 'Bölge':
        import plotly.express as px
        df = getBolgeData(musteri_or_grup=musteri_or_grup, model_tipi=model)
        df.columns = [c.strip() for c in df.columns]

        fig = px.bar(
            df,
            x='BOLGE',
            y=['NEGATIF_OVERRIDE_ORAN', 'POZITIF_OVERRIDE_ORAN', 'OVERRIDE_ORAN'],
            barmode='group',
            color_discrete_map={
                'NEGATIF_OVERRIDE_ORAN': '#dc2626',
                'POZITIF_OVERRIDE_ORAN': '#16a34a',
                'OVERRIDE_ORAN':         '#3b82f6',
            },
            text_auto=True,
        )
        fig.update_traces(textfont_size=11, textposition='outside', cliponaxis=False)
        fig.update_layout(
            title=dict(text='Bölgelere Göre Override Dağılımı', x=0.5, font=dict(size=18, color='#ffffff')),
            width=1200,
            xaxis_title='Bölge',
            yaxis_title='Oran (%)',
            template='plotly_white',
            paper_bgcolor='#1e293b',
            plot_bgcolor='#0f172a',
            font=dict(color='#94a3b8'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                        font=dict(color='#94a3b8')),
            margin=dict(t=80, r=20, b=60, l=60),
        )
        fig.update_xaxes(title_text='Bölge', title_font=dict(color='#ffffff'), tickfont=dict(color='#94a3b8'), type='category')
        fig.update_yaxes(title_text='Oran (%)', title_font=dict(color='#ffffff'), tickfont=dict(color='#94a3b8'))

        return jsonify({
            'table':   df.to_dict(orient='records'),
            'columns': list(df.columns),
            'figure':  json.loads(fig.to_json()),
        })

    if tab == 'Overall':
        import plotly.express as px
        df = getOverallData(musteri_or_grup=musteri_or_grup, model_tipi=model)
        if df.empty:
            return jsonify({'table': [], 'columns': [], 'figure': {}, 'msg': 'Veri bulunamadı.'})

        fig = px.bar(
            df,
            x=df.columns[0],
            y=['NEGATIF_ADET', 'POZITIF_ADET'],
            barmode='group',
            color_discrete_map={'NEGATIF_ADET': '#dc2626', 'POZITIF_ADET': '#16a34a'},
            text_auto=True,
        )
        fig.update_traces(textfont_size=11, textposition='outside', cliponaxis=False)
        fig.update_layout(
            title=dict(text='Genel Bakış', x=0.5, font=dict(size=18, color='#ffffff')),
            width=1200,
            xaxis_title='Özet',
            yaxis_title='Adet',
            template='plotly_white',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                        font=dict(color='#94a3b8')),
        )
        fig.update_xaxes(title_font=dict(color='#ffffff'), tickfont=dict(color='#94a3b8'))
        fig.update_yaxes(title_font=dict(color='#ffffff'), tickfont=dict(color='#94a3b8'))
        fig.update_xaxes(type='category')

        return jsonify({
            'table':   df.to_dict(orient='records'),
            'columns': list(df.columns),
            'figure':  json.loads(fig.to_json()),
        })

    return jsonify({'table': [], 'columns': [], 'figure': {}})


# ---------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(port=8888, debug=True)


