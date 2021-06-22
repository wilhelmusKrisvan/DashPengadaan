import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc  # trs tgl pake aja ini nya
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date
from datetime import timedelta
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from app import app

# connect = 'mysql+pymysql://admindw:admindw@192.168.1.1/amigodw'
connect = 'mysql+pymysql://admindw:admindw@10.10.10.38/amigodw'
conn = create_engine(connect)

dd = pd.read_sql('select * from dim_STRIP', conn)
fd = pd.read_sql('select * from dim_SUPPLIERR', conn)

ked_ukur = ['Kategori', 'Lini Strip']
kel_jen = ['Pria', 'Wanita', 'Anak', 'Sepatu']
stripAll = dd['kode_strip'].dropna().unique()
supplyAll = fd['kode_supplier'].dropna()
tokoAll = ['BIMBO', 'GRANADA', 'KLATEN', 'DINASTI', 'PEDAN', 'SUKOHARJO', 'BOYOLALI', 'WONOSARI', 'KARANGANYAR']
frekWaktu = {'Harian': 'tgl_masuk',
             'Mingguan': 'str_to_date(concat(yearweek(fact_PENGADAAN.tgl_masuk), " Sunday"), "%%X%%V %%W")',
             'Bulanan': 'date_format(tgl_masuk, "%%Y-%%m")',
             'Kuartal': 'concat(year(tgl_masuk)," ", quarter(tgl_masuk))',
             'Semester': 'wk.semester',
             'Tahunan': 'wk.tahun',
             'Puasa':'wk.puasa',
             'Sisa Puasa':'wk.sisa_puasa',
             'Nyadran':'wk.nyadran',
             'Rasulan':'wk.rasulan',
             'Suro':'wk.suro',
             'Natal':'wk.natal',
             'Sekolah':'wk.sekolah'}

def cardGenerator(judul, satuan, warna):
    card = dbc.Card(
        dbc.CardBody([
            html.P(judul, className='card-title', style={'textAlign': 'center', 'fontSize': 15, 'color': 'white'}),
            html.P(satuan + f"0", style={'textAlign': 'center', 'fontSize': 20, 'color': warna}, className='card-text')
        ])
    )
    return card

card_filterPembelian = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                dbc.Card(className='card border-light mb-3' 'card text-white bg-primary mb-3', children=[
                    html.H6('Toko: ', style={'margin': '10px 0px 0px 25px', 'color': 'white'}, className='card-title'),
                    dcc.Dropdown(
                        id='filter-toko',
                        options=[{'label': i, 'value': i} for i in tokoAll],
                        value=[],
                        multi=True,
                        style={'width': '100%', 'color': 'black', 'margin': '0px'},
                        className='card-body'
                    ),
                ]),
            ], width=3),
            # dbc.Col([
            #     dbc.Card(className='card border-light mb-3' 'card text-white bg-primary mb-3', children=[
            #         html.H6('Supplier: ', style={'margin': '10px 0px 0px 25px', 'color': 'white'},
            #                 className='card-title'),
            #         dcc.Dropdown(
            #             id='filter-supplier',
            #             options=[{'label': i, 'value': i} for i in supplyAll],
            #             value=[],
            #             multi=True,
            #             style={'width': '100%', 'color': 'black', 'margin': '0px'},
            #             className='card-body'
            #         ),
            #     ]),
            # ], width=2),
            dbc.Col([
                dbc.Card(className='card border-light mb-3' 'card text-white bg-primary mb-3', children=[
                    html.H6('Kedalaman: ', style={'margin': '10px 0px 0px 25px', 'color': 'white'},
                            className='card-title'),
                    dcc.RadioItems(
                        id='pengukuran',
                        options=[{'label': i, 'value': i} for i in ked_ukur],
                        value=ked_ukur[0],
                        style={'width': '100%', 'color': 'white', 'padding-bottom': '0px', 'padding-top': '0.7rem'},
                        className='card-body',
                        labelStyle={'display': 'block'}
                    ),
                ]),
            ], width=2),
            dbc.Col([
                html.Div([
                    dbc.Card(className='card border-light mb-3' 'card text-white bg-primary mb-3', children=[
                        html.H6('Jenis Kategori: ', style={'margin': '10px 0px 0px 25px', 'color': 'white', },
                                className='card-title'),
                        dcc.Dropdown(
                            id='filter-kategori',
                            options=[{'label': i, 'value': i[0:1]} for i in kel_jen],
                            style={'width': '100%', 'color': 'black'},
                            multi=True,
                            value=[],
                            className='card-body'
                        ),
                    ])
                ], id='div-kategori'),
                html.Div(children=[
                    dbc.Card(className='card border-light mb-3' 'card text-white bg-primary mb-3', children=[
                        html.H6('Kode Strip: ', style={'margin': '10px 0px 0px 25px', 'color': 'white', },
                                className='card-title'),
                        dcc.Dropdown(
                            id='filter-strip',
                            options=[{'label': i, 'value': i} for i in stripAll],
                            style={'width': '100%', 'color': 'black'},
                            multi=True,
                            value=[],
                            className='card-body',
                        ),
                    ])
                ], id='div-strip'),
            ], width=2),
            dbc.Col([
                dbc.Card(className='card border-light mb-3' 'card text-white bg-primary mb-3', children=[
                    html.H6('Range Tanggal: ', style={'margin': '10px 0px 0px 25px', 'color': 'white'},
                            className='card-title'),
                    dcc.DatePickerRange(
                        id='date',
                        start_date=date(2013, 1, 1),
                        end_date=date(2015, 12, 31),
                        display_format='YYYY-MM-DD',
                        className='card-body'
                    )
                ]),
            ], width=3),
            dbc.Col([
                dbc.Card(className='card border-light mb-3' 'card text-white bg-primary mb-3', children=[
                    html.H6('Frekuensi Waktu: ', style={'margin': '10px 0px 0px 25px', 'color': 'white'},
                            className='card-title'),
                    dcc.Dropdown(
                        id='filter-waktu',
                        value='date_format(tgl_masuk, "%%Y-%%m")',
                        clearable=False,
                        style={'width': '100%', 'color': 'black'},
                        className='card-body'
                    ),
                ]),
            ], width=2)
        ]),
    ], style={'padding':'5px 5px 0px 5px'})
], className='card text-white bg-dark mb-3' 'card border-primary mb-3')

card_mainBeli = dbc.Card([
    dbc.CardBody([
        html.H3('Grafik Realisasi Pembelian Barang', style={'color': 'white'}),
        dbc.Spinner([
            dcc.Graph(
                style={'height': 500},
                id='realisasi-beli',
            ),
        ], size='md', color='info', type='grow')
    ])
], className='card border-success mb-3')

card_beliNetto = dbc.Card([
    dbc.CardBody([
        html.H3('Grafik Pembelian Konsinyasi Barang', style={'color': 'white'}),
        html.H6('Grouping', style={'color': 'white'}),
        dcc.RadioItems(
            id='radio-beliNetto',
            options=[
                {'label': 'Toko', 'value': 'nama_toko'},
                {'label': 'Kategori', 'value': 'kel_jns'},
                {'label': 'Lini', 'value': 'kode_strip'},
                # {'label': 'Supply', 'value': 'kode_supplier'},
            ],
            labelStyle={'margin-right':'10px'},
            value='nama_toko'
        ),
        dbc.Spinner([
            dcc.Graph(
                style={'height': 500},
                id='beli-netto',
            ),
        ], size='md', color='info', type='grow')
    ])
], className='card border-success mb-3')

card_beliKonsi = dbc.Card([
    dbc.CardBody([
        html.H3('Grafik Pembelian Non Konsinyasi Barang', style={'color': 'white'}),
        html.H6('Grouping', style={'color': 'white'}),
        dcc.RadioItems(
            id='radio-beliNonKonsi',
            options=[
                {'label': 'Toko', 'value': 'nama_toko'},
                {'label': 'Kategori', 'value': 'kel_jns'},
                {'label': 'Lini', 'value': 'kode_strip'},
                # {'label': 'Supply', 'value': 'kode_supplier'},
            ],
            labelStyle={'margin-right':'10px'},
            value='nama_toko'
        ),
        dbc.Spinner([
            dcc.Graph(
                style={'height': 500},
                id='beli-konsi',
            ),
        ], size='md', color='info', type='grow')
    ])
], className='card border-success mb-3')

card_mainRetur = dbc.Card([
    dbc.CardBody([
        html.H3('Grafik Realisasi Retur Barang', style={'color': 'white'}),
        dbc.Spinner([
            dcc.Graph(
                style={'height': 500},
                id='realisasi-retur',
            ),
        ], size='md', color='info', type='grow')
    ])
], className='card border-info mb-3')

card_returNetto = dbc.Card([
    dbc.CardBody([
        html.H3('Grafik Retur Konsinyasi Barang', style={'color': 'white'}),
        html.H6('Grouping', style={'color': 'white'}),
        dcc.RadioItems(
            id='radio-returNetto',
            options=[
                {'label': 'Toko', 'value': 'nama_toko'},
                {'label': 'Kategori', 'value': 'kel_jns'},
                {'label': 'Lini', 'value': 'kode_strip'},
                # {'label': 'Supply', 'value': 'kode_supplier'},
            ],
            labelStyle={'margin-right':'10px'},
            value='nama_toko'
        ),
        dbc.Spinner([
            dcc.Graph(
                style={'height': 500},
                id='retur-netto',
            ),
        ], size='md', color='info', type='grow')
    ])
], className='card border-info mb-3')

card_returKonsi = dbc.Card([
    dbc.CardBody([
        html.H3('Grafik Retur Non Konsinyasi Barang', style={'color': 'white'}),
        html.H6('Grouping', style={'color': 'white'}),
        dcc.RadioItems(
            id='radio-returNonKonsi',
            options=[
                {'label': 'Toko', 'value': 'nama_toko'},
                {'label': 'Kategori', 'value': 'kel_jns'},
                {'label': 'Lini', 'value': 'kode_strip'},
                # {'label': 'Supply', 'value': 'kode_supplier'},
            ],
            labelStyle={'margin-right':'10px'},
            value='nama_toko'
        ),
        dbc.Spinner([
            dcc.Graph(
                style={'height': 500},
                id='retur-konsi',
            ),
        ], size='md', color='info', type='grow')
    ])
], className='card border-info mb-3')

layout = html.Div([
    # html.Div([
    #     dbc.NavbarSimple(
    #         [
    #             dbc.NavItem(dbc.NavLink('HOME', href='/')),
    #         ],
    #         brand='Amigo Group',
    #         brand_href='/',
    #         color='#375a7f',
    #         className='navbar navbar-expand-lg navbar-dark bg-primary'
    #     ),
    # ], style={'width': '100%', 'position': 'sticky', 'top': '0', 'zIndex': '3'}),
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1('Dashboard Transaksi Pengadaan Barang', style={'text-align': 'center', 'color': 'white'}),
                    width=12)
        ]),
        dbc.Row([
            dbc.Col([
                card_filterPembelian,
            ]),
        ], style={'margin': '15px 0px 0px 0px', 'position': 'sticky', 'zIndex': '3', 'top': '70px'}),
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.Spinner([
                        dbc.CardBody([
                            html.P('Jumlah Total Beli Barang', className='card-title',
                                   style={'textAlign': 'center', 'fontSize': 15, 'color': 'white'}),
                            html.P(id='beli',
                                   style={'textAlign': 'center', 'fontSize': 20, 'color': 'rgb(55, 158, 227)'},
                                   className='card-text'),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.P('Jumlah Beli Barang Non Konsinyasi', className='card-title',
                                                   style={'textAlign': 'center', 'fontSize': 15, 'color': 'white'}),
                                            html.P(id='beliNonKonsi',
                                                   style={'textAlign': 'center', 'fontSize': 17,
                                                          'color': 'rgb(34, 255, 0)'},
                                                   className='card-text')
                                        ])
                                        , className='card border-success mb-3')
                                ]),
                                dbc.Col([
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.P('Jumlah Beli Barang Konsinyasi', className='card-title',
                                                   style={'textAlign': 'center', 'fontSize': 15, 'color': 'white'}),
                                            html.P(id='beliNetto',
                                                   style={'textAlign': 'center', 'fontSize': 17,
                                                          'color': 'rgb(34, 255, 0)'},
                                                   className='card-text')

                                        ])
                                        , className='card border-success mb-3')
                                ]),
                                dbc.Col([
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.P('Jumlah Beli Barang Lini ZZ', className='card-title',
                                                   style={'textAlign': 'center', 'fontSize': 15, 'color': 'white'}),
                                            html.P(id='ZZ',
                                                   style={'textAlign': 'center', 'fontSize': 17,
                                                          'color': 'rgb(255, 208, 0)'},
                                                   className='card-text')

                                        ])
                                        , className='card border-success mb-3'),
                                ]),
                            ])
                        ])
                    ], size='lg', color='info', type='grow')
                    , className='card border-success mb-3'),
            ], width=6),
            dbc.Col([
                dbc.Card(
                    dbc.Spinner([
                        dbc.CardBody([
                            html.P('Jumlah Total Retur Barang', className='card-title',
                                   style={'textAlign': 'center', 'fontSize': 15, 'color': 'white'}),
                            html.P(id='retur',
                                   style={'textAlign': 'center', 'fontSize': 20, 'color': 'rgb(55, 158, 227)'},
                                   className='card-text'),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.P('Jumlah Retur Barang Non Konsinyasi', className='card-title',
                                                   style={'textAlign': 'center', 'fontSize': 15, 'color': 'white'}),
                                            html.P(id='returNonKonsi',
                                                   style={'textAlign': 'center', 'fontSize': 17,
                                                          'color': 'rgb(34, 255, 0)'},
                                                   className='card-text')

                                        ])
                                        ,className='card border-info mb-3')
                                ]),
                                dbc.Col([
                                    dbc.Card(
                                        dbc.CardBody([
                                            html.P('Jumlah Retur Barang Konsinyasi', className='card-title',
                                                   style={'textAlign': 'center', 'fontSize': 15, 'color': 'white'}),
                                            html.P(id='returNetto',
                                                   style={'textAlign': 'center', 'fontSize': 17,
                                                          'color': 'rgb(34, 255, 0)'},
                                                   className='card-text')
                                        ])
                                        , className='card border-info mb-3')
                                ]),
                            ], style={'margin-top': '38px'})
                        ])
                    ], size='lg', color='info', type='grow')
                    , className='card border-info mb-3')
            ], width=6),
        ], style={'margin': '15px 0px 0px 0px'}),
        dbc.Row([
            dbc.Col([
                card_mainBeli
            ]),
        ], style={'margin': '15px 0px 0px 0px'}),
        dbc.Row([
            dbc.Col([
                card_beliKonsi
            ]),
            dbc.Col([
                card_beliNetto
            ]),
        ], style={'margin': '15px 0px 0px 0px'}),
        dbc.Row([
            dbc.Col([
                card_mainRetur
            ]),
        ], style={'margin': '15px 0px 0px 0px'}),
        dbc.Row([
            dbc.Col([
                card_returKonsi
            ]),
            dbc.Col([
                card_returNetto
            ]),
        ], style={'margin': '15px 0px 0px 0px'}),
    ], fluid=True)
], style={'width': '100%'})


# @CALLBACK FILTER
@app.callback(
    Output('filter-waktu', 'options'),
    Input('date', 'end_date'),
    Input('date', 'start_date'),
)
def change_stateDate(end_date, start_date):
    endDateObj = date.fromisoformat(end_date)
    startDateObj = date.fromisoformat(start_date)
    delta = endDateObj - startDateObj
    if delta.days < 2:
        return [{'label': i, 'value': i, 'disabled': True} for i in frekWaktu]
    if delta.days < 14:
        return [{'label': k, 'value': frekWaktu[k]} for k in frekWaktu if k in ('Harian')]
    elif delta.days < 60:
        return [{'label': k, 'value': frekWaktu[k]} for k in frekWaktu if k in ('Harian', 'Mingguan')]
    elif delta.days < 180:
        return [{'label': k, 'value': frekWaktu[k]} for k in frekWaktu if k not in ('Kuartal', 'Semester', 'Tahunan', 'Puasa','Sisa Puasa','Nyadran','Rasulan','Suro','Natal','Sekolah')]
    elif delta.days < 365:
        return [{'label': k, 'value': frekWaktu[k]} for k in frekWaktu if k not in ('Semester', 'Tahunan','Puasa','Sisa Puasa','Nyadran','Rasulan','Suro','Natal','Sekolah')]
    elif delta.days < 730:
        return [{'label': k, 'value': frekWaktu[k]} for k in frekWaktu if k not in ('Tahunan', 'Puasa','Sisa Puasa','Nyadran','Rasulan','Suro','Natal','Sekolah')]
    else:
        return [{'label': k, 'value': frekWaktu[k]} for k in frekWaktu]

@app.callback(
    Output('div-strip', 'style'),
    Output('div-kategori', 'style'),
    Output('filter-strip', 'value'),
    Output('filter-kategori', 'value'),
    Input('pengukuran', 'value')
)
def change_stateDeep(ukur):
    if ukur == 'Kategori':
        return {'color': 'black', 'display': 'none'}, {'color': 'black', 'display': 'block'}, [], []
    if ukur == 'Lini Strip':
        return {'color': 'black', 'display': 'block'}, {'color': 'black', 'display': 'none'}, [], []


# CARD ZZ
@app.callback(
    Output('ZZ', 'children'),
    Input('filter-toko', 'value'),
    # Input('filter-supplier', 'value'),
    Input('filter-strip', 'value'),
    Input('filter-kategori', 'value'),
    Input('date', 'start_date'),
    Input('date', 'end_date'),
    Input('filter-waktu', 'value'),
)
def update_cardZZ(toko, strip, kategori, startDate, endDate, frekWak):
    col_kategori = dd['kel_jns'].dropna().unique()
    df_zz = pd.read_sql('select sum(sub_total) as total, kode_strip '
                        'from fact_PENGADAAN '
                        'inner join dim_STRIP on fact_PENGADAAN.strip_key = dim_STRIP.strip_key '
                        'inner join dim_SUPPLIERR on fact_PENGADAAN.supplier_key = dim_SUPPLIERR.supplier_key '
                        'inner join dim_WAKTU wk on fact_PENGADAAN.tgl_masuk = wk.tanggal '
                        'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
                        'where tgl_masuk between %(startDate)s and %(endDate)s '
                        'and fact_PENGADAAN.jenis_transaksi = "BELI" '
                        'and tk.nama_toko in %(toko)s '
                        #'and dim_SUPPLIERR.kode_supplier in %(supply)s '
                        'and dim_STRIP.kel_jns in %(kel_jns)s '
                        'and dim_STRIP.kode_strip in %(strip)s '
                        'and {kolom} != %(value)s '
                        'group by kode_strip '.format(kolom=frekWak if frekWak in ('wk.nyadran','wk.sisa_puasa','wk.puasa','wk.suro','wk.rasulan','wk.natal','wk.sekolah') else 'wk.tanggal'), conn,
                        params={'toko': tuple(toko) if len(toko) != 0 or None else tuple(tokoAll),
                                #'supply': tuple(supply) if len(supply) != 0 else tuple(supplyAll),
                                'kel_jns': tuple(kategori) if len(kategori) != 0 else tuple(col_kategori),
                                'strip': tuple(strip) if len(strip) != 0 else tuple(stripAll),
                                'startDate': startDate,
                                'endDate': endDate,
                                'value': '-' if frekWak in ('wk.nyadran','wk.sisa_puasa','wk.puasa','wk.suro','wk.rasulan','wk.natal','wk.sekolah') else '1',})
    zz = df_zz.loc[df_zz['kode_strip'] =='ZZ', ('total')].agg({'total': np.sum})
    txtZZ = 'Rp ' + f"{zz.iloc[-1]:,.0f}"
    return txtZZ


# BELI
@app.callback(
    Output('realisasi-beli', 'figure'),
    Output('beli', 'children'),
    Input('filter-toko', 'value'),
    # Input('filter-supplier', 'value'),
    Input('filter-strip', 'value'),
    Input('filter-kategori', 'value'),
    Input('date', 'start_date'),
    Input('date', 'end_date'),
    Input('filter-waktu', 'value'),
)
def update_beli(toko, strip, kategori, startDate, endDate, frekWak):
    col_kategori = dd['kel_jns'].dropna().unique()
    df_beliAll = pd.read_sql('select sum(sub_total) as total, {tgl} as "tanggal" '
                             'from fact_PENGADAAN '
                             'inner join dim_STRIP on fact_PENGADAAN.strip_key = dim_STRIP.strip_key '
                             'inner join dim_SUPPLIERR on fact_PENGADAAN.supplier_key = dim_SUPPLIERR.supplier_key '
                             'inner join dim_WAKTU on fact_PENGADAAN.tgl_masuk = dim_WAKTU.tanggal '
                             'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
                             'inner join dim_WAKTU wk on fact_PENGADAAN.tgl_masuk = wk.tanggal '
                             'where tgl_masuk between %(startDate)s and %(endDate)s '
                             'and fact_PENGADAAN.jenis_transaksi = "BELI" '
                             'and tk.nama_toko in %(toko)s '
                             #'and dim_SUPPLIERR.kode_supplier in %(supply)s '
                             'and dim_STRIP.kel_jns in %(kel_jns)s '
                             'and dim_STRIP.kode_strip in %(strip)s '
                             'and {kolom} != %(value)s '
                             'group by {tgl} '
                             'order by {tgl} '.format(tgl=frekWak, kolom=frekWak if frekWak in ('wk.nyadran','wk.sisa_puasa','wk.puasa','wk.suro','wk.rasulan','wk.natal','wk.sekolah') else 'wk.tanggal'), conn,
                             params={'toko': tuple(toko) if len(toko) != 0 or None else tuple(tokoAll),
                                     #'supply': tuple(supply) if len(supply) != 0 else tuple(supplyAll),
                                     'kel_jns': tuple(kategori) if len(kategori) != 0 else tuple(col_kategori),
                                     'strip': tuple(strip) if len(strip) != 0 else tuple(stripAll),
                                     'startDate': startDate,
                                     'endDate': endDate,
                                     'value': '-' if frekWak in ('wk.nyadran','wk.sisa_puasa','wk.puasa','wk.suro','wk.rasulan','wk.natal','wk.sekolah') else '1',})
    df_beli = pd.read_sql('select sum(sub_total) as total, {tgl} as "tanggal", status_konsinyasi '
                          'from fact_PENGADAAN '
                          'inner join dim_STRIP on fact_PENGADAAN.strip_key = dim_STRIP.strip_key '
                          'inner join dim_SUPPLIERR on fact_PENGADAAN.supplier_key = dim_SUPPLIERR.supplier_key '
                          'inner join dim_WAKTU on fact_PENGADAAN.tgl_masuk = dim_WAKTU.tanggal '
                          'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
                          'inner join dim_WAKTU wk on fact_PENGADAAN.tgl_masuk = wk.tanggal '
                          'where tgl_masuk between %(startDate)s and %(endDate)s '
                          'and fact_PENGADAAN.jenis_transaksi = "BELI" '
                          'and tk.nama_toko in %(toko)s '
                          #'and dim_SUPPLIERR.kode_supplier in %(supply)s '
                          'and dim_STRIP.kel_jns in %(kel_jns)s '
                          'and dim_STRIP.kode_strip in %(strip)s '
                          'and {kolom} != %(value)s '
                          'group by {tgl}, status_konsinyasi '
                          'order by {tgl}, status_konsinyasi '.format(tgl=frekWak, kolom=frekWak if frekWak in ('wk.nyadran','wk.sisa_puasa','wk.puasa','wk.suro','wk.rasulan','wk.natal','wk.sekolah') else 'wk.tanggal'), conn,
                          params={'toko': tuple(toko) if len(toko) != 0 or None else tuple(tokoAll),
                                  #'supply': tuple(supply) if len(supply) != 0 else tuple(supplyAll),
                                  'kel_jns': tuple(kategori) if len(kategori) != 0 else tuple(col_kategori),
                                  'strip': tuple(strip) if len(strip) != 0 else tuple(stripAll),
                                  'startDate': startDate,
                                  'endDate': endDate,
                                  'value': '-' if frekWak in ('wk.nyadran', 'wk.sisa_puasa', 'wk.puasa', 'wk.suro', 'wk.rasulan','wk.natal','wk.sekolah') else '1', })
    beli = df_beli.loc[:, ('total')].agg({'total': np.sum})
    txtBeli = 'Rp ' + f"{beli.iloc[-1]:,.0f}"
    if (len(df_beli['tanggal']) != 0 or len(df_beli['total']) != 0):
        fig = px.line(df_beli, x=df_beli['tanggal'], y=df_beli['total'], color=df_beli['status_konsinyasi'],template='plotly_dark')
        fig.update_layout(xaxis=dict(tickvals=df_beli['tanggal'].unique()), paper_bgcolor='#303030',
                          xaxis_title="Tanggal",
                          yaxis_title="Total Rupiah (Rupiah)",
                          yaxis=dict(tickformat=",.2f"))
        #fig.update_layout(paper_bgcolor='#303030')
        fig.update_traces(mode='lines+markers')
        fig.add_bar(name='all', x=df_beliAll['tanggal'], y=df_beliAll['total'])
        return fig, txtBeli
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig, txtBeli


# BELINETTO
@app.callback(
    Output('beli-netto', 'figure'),
    Output('beliNetto', 'children'),
    Input('radio-beliNetto', 'value'),
    Input('filter-toko', 'value'),
    #Input('filter-supplier', 'value'),
    Input('filter-strip', 'value'),
    Input('filter-kategori', 'value'),
    Input('date', 'start_date'),
    Input('date', 'end_date'),
    Input('filter-waktu', 'value'),
)
def update_beliNetto(radio, toko, strip, kategori, startDate, endDate, frekWak):
    col_strip = list(dd[dd.kode_strip!='ZZ'].kode_strip.dropna().unique())
    col_kategori = dd['kel_jns'].dropna().unique()
    # df_belAll = pd.read_sql('select sum(sub_total) as total, {tgl} as "tanggal" '
    #                           'from fact_PENGADAAN '
    #                           'inner join dim_STRIP on fact_PENGADAAN.strip_key = dim_STRIP.strip_key '
    #                           'inner join dim_SUPPLIERR on fact_PENGADAAN.supplier_key = dim_SUPPLIERR.supplier_key '
    #                           'inner join dim_WAKTU on fact_PENGADAAN.tgl_masuk = dim_WAKTU.tanggal '
    #                           'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
    #                           'where tgl_masuk between %(startDate)s and %(endDate)s '
    #                           'and fact_PENGADAAN.jenis_transaksi = "BELI" '
    #                           'and fact_PENGADAAN.status_konsinyasi = "KONSINYASI" '
    #                           'and dim_STRIP.kode_strip != "ZZ" '
    #                           'group by {tgl} '
    #                           'order by {tgl} '.format(tgl=frekWak),conn,
    #                           params = {'startDate': startDate,
    #                                     'endDate': endDate,})
    df_beli = pd.read_sql('select sum(sub_total) as total, {tgl} as "tanggal",{radio} '
                          'from fact_PENGADAAN '
                          'inner join dim_STRIP on fact_PENGADAAN.strip_key = dim_STRIP.strip_key '
                          'inner join dim_SUPPLIERR on fact_PENGADAAN.supplier_key = dim_SUPPLIERR.supplier_key '
                          'inner join dim_WAKTU on fact_PENGADAAN.tgl_masuk = dim_WAKTU.tanggal '
                          'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
                          'inner join dim_WAKTU wk on fact_PENGADAAN.tgl_masuk = wk.tanggal '
                          'where tgl_masuk between %(startDate)s and %(endDate)s '
                          'and fact_PENGADAAN.jenis_transaksi = "BELI" '
                          'and fact_PENGADAAN.status_konsinyasi = "KONSINYASI" '
                          'and tk.nama_toko in %(toko)s '
                          #'and dim_SUPPLIERR.kode_supplier in %(supply)s '
                          'and dim_STRIP.kel_jns in %(kel_jns)s '
                          'and dim_STRIP.kode_strip in %(strip)s '
                          #'and dim_STRIP.kode_strip != "ZZ" '
                          'and {kolom} != %(value)s '
                          'group by {tgl}, {radio} '
                          'order by {tgl} '.format(radio=radio, tgl=frekWak, kolom=frekWak if frekWak in ('wk.nyadran','wk.sisa_puasa','wk.puasa','wk.suro','wk.rasulan','wk.natal','wk.sekolah') else 'wk.tanggal'), conn,
                          params={'toko': tuple(toko) if len(toko) != 0 or None else tuple(tokoAll),
                                  # 'supply': tuple(supply) if len(supply) != 0 else tuple(supplyAll),
                                  'kel_jns': tuple(kategori) if len(kategori) != 0 else tuple(col_kategori),
                                  'strip': tuple(strip) if len(strip) != 0 else tuple(col_strip),
                                  'startDate': startDate,
                                  'endDate': endDate,
                                  'value': '-' if frekWak in ('wk.nyadran', 'wk.sisa_puasa', 'wk.puasa', 'wk.suro', 'wk.rasulan','wk.natal','wk.sekolah') else '1',})
    beli = df_beli.loc[:, ('total')].agg({'total': np.sum})
    txtBeli = 'Rp ' + f"{beli.iloc[-1]:,.0f}"
    if (len(df_beli['tanggal']) != 0 or len(df_beli['total']) != 0):
        fig = px.line(df_beli, x=df_beli['tanggal'], y=df_beli['total'], color=df_beli[radio],template='plotly_dark')
        fig.update_layout(xaxis=dict(tickvals=df_beli['tanggal'].unique()), paper_bgcolor='#303030',
                          xaxis_title="Tanggal",
                          yaxis_title="Total Rupiah (Rupiah)",
                          yaxis=dict(tickformat=",.2f"))
        #fig.update_layout(paper_bgcolor='#303030')
        fig.update_traces(mode='lines+markers')
        # fig.add_scatter(name='all', x=df_belAll['tanggal'], y=df_belAll['total'], marker={'color': 'rgb(0,0,90)'})
        return fig, txtBeli
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig, txtBeli


# BELIKON
@app.callback(
    Output('beli-konsi', 'figure'),
    Output('beliNonKonsi', 'children'),
    Input('radio-beliNonKonsi', 'value'),
    Input('filter-toko', 'value'),
    # Input('filter-supplier', 'value'),
    Input('filter-strip', 'value'),
    Input('filter-kategori', 'value'),
    Input('date', 'start_date'),
    Input('date', 'end_date'),
    Input('filter-waktu', 'value'),
)
def update_beliNonKonsi(radio, toko, strip, kategori, startDate, endDate, frekWak):
    col_strip = list(dd[dd.kode_strip != 'ZZ'].kode_strip.dropna().unique())
    col_kategori = dd['kel_jns'].dropna().unique()
    # df_belAll = pd.read_sql('select sum(sub_total) as total, {tgl} as "tanggal" '
    #                           'from fact_PENGADAAN '
    #                           'inner join dim_STRIP on fact_PENGADAAN.strip_key = dim_STRIP.strip_key '
    #                           'inner join dim_SUPPLIERR on fact_PENGADAAN.supplier_key = dim_SUPPLIERR.supplier_key '
    #                           'inner join dim_WAKTU on fact_PENGADAAN.tgl_masuk = dim_WAKTU.tanggal '
    #                           'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '

    #                           'where tgl_masuk between %(startDate)s and %(endDate)s '
    #                           'and fact_PENGADAAN.jenis_transaksi = "BELI" '
    #                           'and fact_PENGADAAN.status_konsinyasi = "NON KONSINYASI" '
    #                           'and dim_STRIP.kode_strip != "ZZ" '
    #                           'group by {tgl} '
    #                           'order by {tgl} '.format(tgl=frekWak),conn,
    #                           params = {'startDate': startDate,
    #                                     'endDate': endDate,})
    df_beli = pd.read_sql('select sum(sub_total) as total, {tgl} as "tanggal",{radio} '
                          'from fact_PENGADAAN '
                          'inner join dim_STRIP on fact_PENGADAAN.strip_key = dim_STRIP.strip_key '
                          'inner join dim_SUPPLIERR on fact_PENGADAAN.supplier_key = dim_SUPPLIERR.supplier_key '
                          'inner join dim_WAKTU on fact_PENGADAAN.tgl_masuk = dim_WAKTU.tanggal '
                          'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
                          'inner join dim_WAKTU wk on fact_PENGADAAN.tgl_masuk = wk.tanggal '
                          'where tgl_masuk between %(startDate)s and %(endDate)s '
                          'and fact_PENGADAAN.jenis_transaksi = "BELI" '
                          'and fact_PENGADAAN.status_konsinyasi = "NON KONSINYASI" '
                          'and tk.nama_toko in %(toko)s '
                          #'and dim_SUPPLIERR.kode_supplier in %(supply)s '
                          'and dim_STRIP.kel_jns in %(kel_jns)s '
                          'and dim_STRIP.kode_strip in %(strip)s '
                          #'and dim_STRIP.kode_strip != "ZZ" '
                          'and {kolom} != %(value)s '
                          'group by {tgl}, {radio} '
                          'order by {tgl} '.format(radio=radio, tgl=frekWak, kolom=frekWak if frekWak in ('wk.nyadran','wk.sisa_puasa','wk.puasa','wk.suro','wk.rasulan','wk.natal','wk.sekolah') else 'wk.tanggal'), conn,
                          params={'toko': tuple(toko) if len(toko) != 0 or None else tuple(tokoAll),
                                  #'supply': tuple(supply) if len(supply) != 0 else tuple(supplyAll),
                                  'kel_jns': tuple(kategori) if len(kategori) != 0 else tuple(col_kategori),
                                  'strip': tuple(strip) if len(strip) != 0 else tuple(col_strip),
                                  'startDate': startDate,
                                  'endDate': endDate,
                                  'value': '-' if frekWak in ('wk.nyadran', 'wk.sisa_puasa', 'wk.puasa', 'wk.suro', 'wk.rasulan','wk.natal','wk.sekolah') else '1',})
    beli = df_beli.loc[:, ('total')].agg({'total': np.sum})
    txtBeli = 'Rp ' + f"{beli.iloc[-1]:,.0f}"
    if (len(df_beli['tanggal']) != 0 or len(df_beli['total']) != 0):
        fig = px.line(df_beli, x=df_beli['tanggal'], y=df_beli['total'], color=df_beli[radio],template='plotly_dark')
        fig.update_layout(xaxis=dict(tickvals=df_beli['tanggal'].unique()), paper_bgcolor='#303030',
                          xaxis_title="Tanggal",
                          yaxis_title="Total Rupiah (Rupiah)",
                          yaxis=dict(tickformat=",.2f")
                          )
        #fig.update_layout(paper_bgcolor='#303030')
        fig.update_traces(mode='lines+markers')
        # fig.add_bar(name='all', x=df_belAll['tanggal'], y=df_belAll['total'], marker={'color': 'rgb(0,0,90)'})
        return fig, txtBeli
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig, txtBeli


# RETUR
@app.callback(
    Output('realisasi-retur', 'figure'),
    Output('retur', 'children'),
    Input('filter-toko', 'value'),
    # Input('filter-supplier', 'value'),
    Input('filter-strip', 'value'),
    Input('filter-kategori', 'value'),
    Input('date', 'start_date'),
    Input('date', 'end_date'),
    Input('filter-waktu', 'value'),
)
def update_retur(toko, strip, kategori, startDate, endDate, frekWak):
    col_kategori = dd['kel_jns'].dropna().unique()
    df_returAll = pd.read_sql('select sum(sub_total) as total, {tgl} as "tanggal" '
                              'from fact_PENGADAAN '
                              'inner join dim_STRIP on fact_PENGADAAN.strip_key = dim_STRIP.strip_key '
                              'inner join dim_SUPPLIERR on fact_PENGADAAN.supplier_key = dim_SUPPLIERR.supplier_key '
                              'inner join dim_WAKTU on fact_PENGADAAN.tgl_masuk = dim_WAKTU.tanggal '
                              'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
                              'inner join dim_WAKTU wk on fact_PENGADAAN.tgl_masuk = wk.tanggal '
                              'where tgl_masuk between %(startDate)s and %(endDate)s '
                              'and fact_PENGADAAN.jenis_transaksi = "RETUR" '
                              'and tk.nama_toko in %(toko)s '
                              #'and dim_SUPPLIERR.kode_supplier in %(supply)s '
                              'and dim_STRIP.kel_jns in %(kel_jns)s '
                              'and dim_STRIP.kode_strip in %(strip)s '
                              'and {kolom} != %(value)s '
                              'group by {tgl} '
                              'order by {tgl} '.format(tgl=frekWak,kolom=frekWak if frekWak in ('wk.nyadran','wk.sisa_puasa','wk.puasa','wk.suro','wk.rasulan','wk.natal','wk.sekolah') else 'wk.tanggal'), conn,
                              params={'toko': tuple(toko) if len(toko) != 0 or None else tuple(tokoAll),
                                      #'supply': tuple(supply) if len(supply) != 0 else tuple(supplyAll),
                                      'kel_jns': tuple(kategori) if len(kategori) != 0 else tuple(col_kategori),
                                      'strip': tuple(strip) if len(strip) != 0 else tuple(stripAll),
                                      'startDate': startDate,
                                      'endDate': endDate,
                                      'value': '-' if frekWak in ('wk.nyadran', 'wk.sisa_puasa', 'wk.puasa', 'wk.suro', 'wk.rasulan','wk.natal','wk.sekolah') else '1',})
    df_retur = pd.read_sql('select sum(sub_total) as total, {tgl} as "tanggal",status_konsinyasi '
                           'from fact_PENGADAAN '
                           'inner join dim_STRIP on fact_PENGADAAN.strip_key = dim_STRIP.strip_key '
                           'inner join dim_SUPPLIERR on fact_PENGADAAN.supplier_key = dim_SUPPLIERR.supplier_key '
                           'inner join dim_WAKTU on fact_PENGADAAN.tgl_masuk = dim_WAKTU.tanggal '
                           'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
                           'inner join dim_WAKTU wk on fact_PENGADAAN.tgl_masuk = wk.tanggal '
                           'where tgl_masuk between %(startDate)s and %(endDate)s '
                           'and fact_PENGADAAN.jenis_transaksi = "RETUR" '
                           'and tk.nama_toko in %(toko)s '
                           #'and dim_SUPPLIERR.kode_supplier in %(supply)s '
                           'and dim_STRIP.kel_jns in %(kel_jns)s '
                           'and dim_STRIP.kode_strip in %(strip)s '
                           'and {kolom} != %(value)s '
                           'group by {tgl}, status_konsinyasi '
                           'order by {tgl}, status_konsinyasi '.format(tgl=frekWak,kolom=frekWak if frekWak in ('wk.nyadran','wk.sisa_puasa','wk.puasa','wk.suro','wk.rasulan','wk.natal','wk.sekolah') else 'wk.tanggal'), conn,
                           params={'toko': tuple(toko) if len(toko) != 0 or None else tuple(tokoAll),
                                   #'supply': tuple(supply) if len(supply) != 0 else tuple(supplyAll),
                                   'kel_jns': tuple(kategori) if len(kategori) != 0 else tuple(col_kategori),
                                   'strip': tuple(strip) if len(strip) != 0 else tuple(stripAll),
                                   'startDate': startDate,
                                   'endDate': endDate,
                                   'value': '-' if frekWak in ('wk.nyadran', 'wk.sisa_puasa', 'wk.puasa', 'wk.suro', 'wk.rasulan','wk.natal','wk.sekolah') else '1',})
    retur = df_retur.loc[:, ('total')].agg({'total': np.sum})
    txtRetur = 'Rp ' + f"{retur.iloc[-1]:,.0f}"
    if (len(df_retur['tanggal']) != 0 or len(df_retur['total']) != 0):
        fig = px.line(df_retur, x=df_retur['tanggal'], y=df_retur['total'], color=df_retur['status_konsinyasi'],template='plotly_dark')
        fig.update_layout(xaxis=dict(tickvals=df_retur['tanggal'].unique()), paper_bgcolor='#303030',
                          xaxis_title="Tanggal",
                          yaxis_title="Total Rupiah (Rupiah)",
                          yaxis=dict(tickformat=",.2f")
                          )
        #fig.update_layout(paper_bgcolor='#303030')
        fig.update_traces(mode='lines+markers')
        fig.add_bar(name='all', x=df_returAll['tanggal'], y=df_returAll['total'])
        return fig, txtRetur
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig, txtRetur


# RETURNEETO
@app.callback(
    Output('retur-netto', 'figure'),
    Output('returNetto', 'children'),
    Input('radio-returNetto', 'value'),
    Input('filter-toko', 'value'),
    #Input('filter-supplier', 'value'),
    Input('filter-strip', 'value'),
    Input('filter-kategori', 'value'),
    Input('date', 'start_date'),
    Input('date', 'end_date'),
    Input('filter-waktu', 'value'),
)
def update_returNetto(radio, toko, strip, kategori, startDate, endDate, frekWak):
    col_kategori = dd['kel_jns'].dropna().unique()
    # df_retAll = pd.read_sql('select sum(sub_total) as total, {tgl} as "tanggal" '
    #                           'from fact_PENGADAAN '
    #                           'inner join dim_STRIP on fact_PENGADAAN.strip_key = dim_STRIP.strip_key '
    #                           'inner join dim_SUPPLIERR on fact_PENGADAAN.supplier_key = dim_SUPPLIERR.supplier_key '
    #                           'inner join dim_WAKTU on fact_PENGADAAN.tgl_masuk = dim_WAKTU.tanggal '
    #                           'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
    #                           'where tgl_masuk between %(startDate)s and %(endDate)s '
    #                           'and fact_PENGADAAN.jenis_transaksi = "RETUR" '
    #                           'and fact_PENGADAAN.status_konsinyasi = "KONSINYASI" '
    #                           'and dim_STRIP.kode_strip != "ZZ" '
    #                           'group by {tgl} '
    #                           'order by {tgl} '.format(tgl=frekWak),conn,
    #                           params = {'startDate': startDate,
    #                                     'endDate': endDate,})
    df_retur = pd.read_sql('select sum(sub_total) as total, {tgl} as "tanggal",{radio} '
                           'from fact_PENGADAAN '
                           'inner join dim_STRIP on fact_PENGADAAN.strip_key = dim_STRIP.strip_key '
                           'inner join dim_SUPPLIERR on fact_PENGADAAN.supplier_key = dim_SUPPLIERR.supplier_key '
                           'inner join dim_WAKTU on fact_PENGADAAN.tgl_masuk = dim_WAKTU.tanggal '
                           'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
                           'inner join dim_WAKTU wk on fact_PENGADAAN.tgl_masuk = wk.tanggal '
                           'where tgl_masuk between %(startDate)s and %(endDate)s '
                           'and fact_PENGADAAN.jenis_transaksi = "RETUR" '
                           'and fact_PENGADAAN.status_konsinyasi = "KONSINYASI" '
                           'and tk.nama_toko in %(toko)s '
                           #'and dim_SUPPLIERR.kode_supplier in %(supply)s '
                           'and dim_STRIP.kel_jns in %(kel_jns)s '
                           'and dim_STRIP.kode_strip in %(strip)s '
                           'and {kolom} != %(value)s '
                           'group by {tgl}, {radio} '
                           'order by {tgl} ASC '.format(radio=radio, tgl=frekWak,kolom=frekWak if frekWak in ('wk.nyadran','wk.sisa_puasa','wk.puasa','wk.suro','wk.rasulan','wk.natal','wk.sekolah') else 'wk.tanggal'), conn,
                           params={'toko': tuple(toko) if len(toko) != 0 or None else tuple(tokoAll),
                                   #'supply': tuple(supply) if len(supply) != 0 else tuple(supplyAll),
                                   'kel_jns': tuple(kategori) if len(kategori) != 0 else tuple(col_kategori),
                                   'strip': tuple(strip) if len(strip) != 0 else tuple(stripAll),
                                   'startDate': startDate,
                                   'endDate': endDate,
                                   'value': '-' if frekWak in ('wk.nyadran', 'wk.sisa_puasa', 'wk.puasa', 'wk.suro', 'wk.rasulan','wk.natal','wk.sekolah') else '1',})
    retur = df_retur.loc[:, ('total')].agg({'total': np.sum})
    txtRetur = 'Rp ' + f"{retur.iloc[-1]:,.0f}"
    if (len(df_retur['tanggal']) != 0 or len(df_retur['total']) != 0):
        fig = px.line(df_retur, x=df_retur['tanggal'], y=df_retur['total'], color=df_retur[radio],template='plotly_dark')
        fig.update_layout(xaxis=dict(tickvals=df_retur['tanggal'].unique()), paper_bgcolor='#303030',
                          xaxis_title="Tanggal",
                          yaxis_title="Total Rupiah (Rupiah)",
                          yaxis=dict(tickformat=",.2f")
                          )
        #fig.update_layout(paper_bgcolor='#303030')
        fig.update_traces(mode='lines+markers')
        # fig.add_scatter(name='all', x=df_retAll['tanggal'], y=df_retAll['total'], marker={'color': 'rgb(0,0,90)'})
        return fig, txtRetur
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig, txtRetur


# RETURKON
@app.callback(
    Output('retur-konsi', 'figure'),
    Output('returNonKonsi', 'children'),
    Input('radio-returNonKonsi', 'value'),
    Input('filter-toko', 'value'),
    #Input('filter-supplier', 'value'),
    Input('filter-strip', 'value'),
    Input('filter-kategori', 'value'),
    Input('date', 'start_date'),
    Input('date', 'end_date'),
    Input('filter-waktu', 'value'),
)
def update_returNonKonsi(radio, toko, strip, kategori, startDate, endDate, frekWak):
    col_kategori = dd['kel_jns'].dropna().unique()
    # df_retAll = pd.read_sql('select sum(sub_total) as total, {tgl} as "tanggal" '
    #                           'from fact_PENGADAAN '
    #                           'inner join dim_STRIP on fact_PENGADAAN.strip_key = dim_STRIP.strip_key '
    #                           'inner join dim_SUPPLIERR on fact_PENGADAAN.supplier_key = dim_SUPPLIERR.supplier_key '
    #                           'inner join dim_WAKTU on fact_PENGADAAN.tgl_masuk = dim_WAKTU.tanggal '
    #                           'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
    #                           'where tgl_masuk between %(startDate)s and %(endDate)s '
    #                           'and fact_PENGADAAN.jenis_transaksi = "RETUR" '
    #                           'and fact_PENGADAAN.status_konsinyasi = "NON KONSINYASI" '
    #                           'and dim_STRIP.kode_strip != "ZZ" '
    #                           'group by {tgl} '
    #                           'order by {tgl} '.format(tgl=frekWak),conn,
    #                           params = {'startDate': startDate,
    #                                     'endDate': endDate,})
    df_retur = pd.read_sql('select sum(sub_total) as total, {tgl} as "tanggal",{radio} '
                           'from fact_PENGADAAN '
                           'inner join dim_STRIP on fact_PENGADAAN.strip_key = dim_STRIP.strip_key '
                           'inner join dim_SUPPLIERR on fact_PENGADAAN.supplier_key = dim_SUPPLIERR.supplier_key '
                           'inner join dim_WAKTU on fact_PENGADAAN.tgl_masuk = dim_WAKTU.tanggal '
                           'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
                           'inner join dim_WAKTU wk on fact_PENGADAAN.tgl_masuk = wk.tanggal '
                           'where tgl_masuk between %(startDate)s and %(endDate)s '
                           'and fact_PENGADAAN.jenis_transaksi = "RETUR" '
                           'and fact_PENGADAAN.status_konsinyasi = "NON KONSINYASI" '
                           'and tk.nama_toko in %(toko)s '
                           #'and dim_SUPPLIERR.kode_supplier in %(supply)s '
                           'and dim_STRIP.kel_jns in %(kel_jns)s '
                           'and dim_STRIP.kode_strip in %(strip)s '
                           'and {kolom} != %(value)s '
                           'group by {tgl}, {radio} '
                           'order by {tgl} '.format(radio=radio, tgl=frekWak,kolom=frekWak if frekWak in ('wk.nyadran','wk.sisa_puasa','wk.puasa','wk.suro','wk.rasulan','wk.natal','wk.sekolah') else 'wk.tanggal'), conn,
                           params={'toko': tuple(toko) if len(toko) != 0 or None else tuple(tokoAll),
                                   #'supply': tuple(supply) if len(supply) != 0 else tuple(supplyAll),
                                   'kel_jns': tuple(kategori) if len(kategori) != 0 else tuple(col_kategori),
                                   'strip': tuple(strip) if len(strip) != 0 else tuple(stripAll),
                                   'startDate': startDate,
                                   'endDate': endDate,
                                   'value': '-' if frekWak in ('wk.nyadran', 'wk.sisa_puasa', 'wk.puasa', 'wk.suro', 'wk.rasulan','wk.natal','wk.sekolah') else '1',})
    retur = df_retur.loc[:, ('total')].agg({'total': np.sum})
    txtRetur = 'Rp ' + f"{retur.iloc[-1]:,.0f}"
    if (len(df_retur['tanggal']) != 0 or len(df_retur['total']) != 0):
        fig = px.line(df_retur, x=df_retur['tanggal'], y=df_retur['total'], color=df_retur[radio],template='plotly_dark')
        fig.update_layout(xaxis=dict(tickvals=df_retur['tanggal'].unique()), paper_bgcolor='#303030',
                          xaxis_title="Tanggal",
                          yaxis_title="Total Rupiah (Rupiah)",
                          yaxis=dict(tickformat=",.2f")
                          )
        #fig.update_layout(paper_bgcolor='#303030')
        fig.update_traces(mode='lines+markers')
        # fig.add_bar(name='all', x=df_retAll['tanggal'], y=df_retAll['total'], marker={'color': 'rgb(0,0,90)'})
        return fig, txtRetur
    else:
        fig = go.Figure().add_annotation(x=2.5, y=2, text="Tidak Ada Data yang Ditampilkan",
                                         font=dict(family="sans serif", size=25, color="crimson"), showarrow=False,
                                         yshift=10)
        return fig, txtRetur