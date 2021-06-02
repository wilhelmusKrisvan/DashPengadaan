# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import dash_bootstrap_components as dbc
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# # from flask_mysqldb import MySQL
# # import
# import pandas as pd
# import numpy as np
# import plotly.express as px
#
# from datetime import date, datetime
# from datetime import timedelta
# from dash.dependencies import Input, Output, State
#
# from sqlalchemy import create_engine
#
# #connect = 'mysql+pymysql://root:@localhost/amigodw'
# connect = 'mysql+pymysql://admindw:admindw@10.10.14.5/amigodw'
# conn = create_engine(connect)
#
# dd = pd.read_sql('select kode_strip,kel_jns from dim_STRIP ',conn)
# fd = pd.read_sql('select kode_supplier from dim_SUPPLIERR ',conn)
#
# #DATA FILTER KONDISI
# ked_ukur=['Kategori','Lini']
# kel_jen=['Pria','Wanita','Anak','Sepatu']
# stripAll = dd['kode_strip'].dropna().unique()
# supplyAll = fd['kode_supplier'].dropna().unique()
# #dd['nama_toko'].unique()
# tokoAll = ['BIMBO','GRANADA','KLATEN','DINASTI','PEDAN','SUKOHARJO','BOYOLALI','WONOSARI','KARANGANYAR']
# frekWaktu = ['Harian', 'Mingguan', 'Bulanan', 'Quartal', 'Semester', 'Tahunan']
#
# #DATA OLAH CARD ORDER
# # jmlnota_tepat = df.loc[(df["order_ontime"]=='TEPAT'),('no_faktur')].agg({'no_faktur':'nunique'})
# # jmlnota_terlambat = df.loc[(df["order_ontime"]!='TEPAT'),('no_faktur')].agg({'no_faktur':'nunique'})
# # jml_total = jmlnota_tepat - jmlnota_terlambat
#
# # def change_option(option):
# #     opsi = pd.read_sql('select kode_toko, kode_strip, kode_supplier from fact_PENGADAAN '
# #                        'inner join dim_SUPPLIERR on dim_SUPPLIERR.supplier_key = fact_PENGADAAN.supplier_key '
# #                        'inner join dim_STRIP on dim_STRIP.strip_key = fact_PENGADAAN.strip_key ',conn)
# #     return [{'label':i,'value':i} for i in opsi[option].dropna().unique()]
#
# card_filterOrder=dbc.Card([
#     dbc.CardBody([
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card(className='card text-white bg-dark mb-3',children=[
#                     html.H5('Toko: ',style={'margin':'10px 0px 0px 25px','color':'white'},className='card-title'),
#                     dcc.Dropdown(
#                         id='filter-tokoOrder',
#                         options=[{'label': i, 'value': i} for i in tokoAll],
#                         value=[],
#                         multi=True,
#                         style={'width': '100%','color':'black','margin':'0px'},
#                         className='card-body'
#                     ),
#                 ]),
#             ],width=2),
#             dbc.Col([
#                 dbc.Card(className='card text-white bg-dark mb-3',children=[
#                     html.H5('Supplier: ', style={'margin':'10px 0px 0px 25px', 'color': 'white'},className='card-title'),
#                     dcc.Dropdown(
#                         id='filter-supplierOrder',
#                         options=[{'label':i,'value':i} for i in supplyAll],
#                         value=[],
#                         multi=True,
#                         style={'width': '100%','color':'black','margin':'0px'},
#                         className='card-body'
#                     ),
#                 ]),
#             ],width=2),
#             dbc.Col([
#                 dbc.Card(className='card text-white bg-dark mb-3',children=[
#                     html.H5('Kedalaman: ', style={'margin':'10px 0px 0px 25px', 'color': 'white'},className='card-title'),
#                     dcc.RadioItems(
#                         id='pengukuranOrder',
#                         options=[{'label': i, 'value': i} for i in ked_ukur],
#                         value=ked_ukur[0],
#                         style={'width': '100%', 'color': 'white'},
#                         className='card-body'
#                     ),
#                 ]),
#             ],width=2),
#             dbc.Col([
#                 html.Div([
#                     dbc.Card(className='card text-white bg-dark mb-3', children=[
#                         html.H5('Jenis Kategori: ', style={'margin': '10px 0px 0px 25px', 'color': 'white', },
#                                 className='card-title'),
#                         dcc.Dropdown(
#                             id='filter-kategoriOrder',
#                             options=[{'label':i,'value':i[0:1]} for i in kel_jen],
#                             value=[],
#                             style={'width': '100%', 'color': 'black'},
#                             multi=True,
#                             className='card-body'
#                         ),
#                     ])
#                 ], id='div-kategoriOrder'),
#                 html.Div(children=[
#                     dbc.Card(className='card text-white bg-dark mb-3',children=[
#                         html.H5('Kode Strip: ', style={'margin':'10px 0px 0px 25px', 'color': 'white',},
#                                 className='card-title'),
#                         dcc.Dropdown(
#                             id='filter-stripOrder',
#                             options=[{'label':i,'value':i} for i in stripAll],
#                             value=[],
#                             style={'width': '100%', 'color': 'black'},
#                             multi=True,
#                             className='card-body',
#                         ),
#                     ])
#                 ], id='div-stripOrder'),
#             ],width=5),
#         ]),
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card(className='card text-white bg-dark mb-3',children=[
#                     html.H5('Range Tanggal: ',style={'margin':'10px 0px 0px 25px','color':'white'},className='card-title'),
#                     dcc.DatePickerRange(
#                         id='dateOrder',
#                         start_date=date(2013,1,1), #date.today()
#                         end_date=date(2015,12,31),
#                         display_format='YYYY-MM-DD',
#                         className='card-body'
#                     )
#                 ]),
#             ],width=4),
#             dbc.Col([
#                 dbc.Card(className='card text-white bg-dark mb-3',children=[
#                     html.H5('Frekuensi Waktu: ', style={'margin':'10px 0px 0px 25px', 'color': 'white'},className='card-title'),
#                     dcc.Dropdown(
#                         id='filter-waktuOrder',
#                         value='str_to_date(concat(date_format(tgl_masuk, "%%Y-%%m"), "-01"), "%%Y-%%m-%%d")',
#                         clearable=False,
#                         style={'width': '100%', 'color': 'black'},
#                         className='card-body'
#                     ),
#                 ]),
#             ],width=2)
#         ])
#     ])
# ],className='card border-light mb-3')
#
# card_stack = dbc.Card([
#     dbc.CardBody([
#         html.H3('Rata - Rata Ketepatan Order',style={'color':'white'}),
#         html.H5('Grouping : ',style={'color':'white'}),
#         dcc.RadioItems(
#             id='radio-rasio',
#             options=[
#                 {'label': 'Toko', 'value': 'nama_toko'},
#                 {'label': 'Kategori', 'value': 'kel_jns'},
#                 # {'label': 'Lini', 'value': 'kode_strip'},
#                 # {'label': 'Supply', 'value': 'kode_supplier'},
#             ],
#             value='nama_toko',
#         ),
#         dbc.Spinner([
#             dcc.Graph(
#                 style={'height': 400},
#                 id='rate-order',
#             ),
#         ],size='md', color='primary', type='border')
#     ])
# ])
#
# card_pie = dbc.Card([
#     dbc.CardBody([
#         html.H3('Rasio Ketepatan Order',style={'color':'white'}),
#         dbc.Spinner([
#             dcc.Graph(
#                 style={'height': 375},
#                 id='percent-order',
#             ),
#         ],size='md', color='primary', type='border')
#     ])
# ])
#
# card_stacked = dbc.Card([
#     dbc.CardBody([
#         html.H3('Rasio Ketepatan Order',style={'color':'white'}),
#         dbc.Spinner([
#             dcc.Graph(
#                 style={'height': 375},
#                 id='sum-order',
#             ),
#         ],size='md', color='primary', type='border')
#     ])
# ])
#
# # def cardGenerator(judul, sumber, satuan, warna):
# #     card = dbc.Card(
# #                 dbc.CardBody([
# #                     html.H4(judul, className='card-title',style={'textAlign':'center','color':'white'}),
# #                     html.P(satuan+f"{sumber.iloc[-1]:,.0f}",style={'textAlign':'center','fontSize':40,'color':warna},className='card-text')
# #                 ])
# #            )
# #     return card
#
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
# # mysql = MySQL(app.server)
#
# app.layout = html.Div([
#     html.Div([
#         dbc.NavbarSimple(
#             [
#                 dbc.NavItem(dbc.NavLink('Halaman Web', href='#')),
#             ],
#             brand='Amigo Group',
#             brand_href='#',
#             color='#001524',
#             dark=True,
#         ),
#     ], style={'width': '100%', 'position': 'sticky', 'top': '0', 'zIndex': '3'}),
#     dbc.Container([
#         dbc.Row([
#             dbc.Col(html.H1('Dashboard Pengadaan Barang', style={'text-align': 'center', 'color': 'white'}), width=12)
#         ]),
#         dbc.Row([
#             dbc.Col([
#                 card_filterOrder,
#             ]),
#         ], style={'margin': '25px 0px 0px 0px'}),
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card(
#                     dbc.CardBody([
#                         html.H4('Jumlah Nota Total', className='card-title',
#                                 style={'textAlign': 'center', 'color': 'white'}),
#                         dbc.Spinner([
#                             html.P(id='jmlTot',
#                                    style={'textAlign': 'center', 'fontSize': 40, 'color': 'rgb(0, 110, 255)'},
#                                    className='card-text')
#                         ],size='md', color='primary', type='border')
#                     ])
#                 )
#             ], width=12, style={'margin': '0px 0px 25px 0px'}),
#             dbc.Col([
#                 dbc.Card(
#                     dbc.CardBody([
#                         html.H4('Jumlah Nota Tepat Waktu', className='card-title',
#                                 style={'textAlign': 'center', 'color': 'white'}),
#                         dbc.Spinner([
#                             html.P(id='jmlTepat',
#                                    style={'textAlign': 'center', 'fontSize': 40, 'color': 'rgb(34, 255, 0)'},
#                                    className='card-text')
#                         ],size='md', color='primary', type='border')
#                     ])
#                 )
#             ], width=6),
#             dbc.Col([
#                 dbc.Card(
#                     dbc.CardBody([
#                         html.H4('Jumlah Nota Terlambat', className='card-title',
#                                 style={'textAlign': 'center', 'color': 'white'}),
#                         dbc.Spinner([
#                             html.P(id='jmlTelat',
#                                    style={'textAlign': 'center', 'fontSize': 40, 'color': 'rgb(255, 208, 0)'},
#                                    className='card-text')
#                         ],size='md', color='primary', type='border')
#                     ])
#                 )
#             ], width=6),
#         ], style={'margin': '25px 0px 0px 0px'}),
#         dbc.Row([
#             dbc.Col([
#                 card_pie
#             ], width=6),
#             dbc.Col([
#                 card_stacked
#             ], width=6),
#         ], style={'margin': '25px 0px 0px 0px'}),
#         dbc.Row([
#             dbc.Col([
#                 card_stack
#             ], width=12),
#         ], style={'margin': '25px 0px 0px 0px'}),
#     ],fluid=True)
# ],style={'width': '100%'})
#
# #@CALLBACK FILTER
# @app.callback(
#     Output('filter-waktuOrder', 'options'),
#     Input('dateOrder','end_date'),
#     Input('dateOrder', 'start_date'),
# )
# def change_stateDate(end_date, start_date):
#     endDateObj = date.fromisoformat(end_date)
#     startDateObj = date.fromisoformat(start_date)
#     delta = endDateObj-startDateObj
#     if delta.days < 2:
#         return [{'label': i, 'value': i, 'disabled': True} for i in frekWaktu]
#     if delta.days <14:
#         return [{'label': 'Harian', 'value': 'tgl_masuk'}]
#     elif delta.days <60:
#         return [{'label': 'Harian', 'value': 'tgl_masuk'},
#                 {'label': 'Mingguan', 'value': 'str_to_date(concat(yearweek(fact_PENGADAAN.tgl_masuk), " Sunday"), "%%X%%V %%W")'},]
#     elif delta.days <180:
#         return [{'label': 'Harian', 'value': 'tgl_masuk'},
#                 {'label': 'Mingguan', 'value': 'str_to_date(concat(yearweek(fact_PENGADAAN.tgl_masuk), " Sunday"), "%%X%%V %%W")'},
#                 {'label': 'Bulanan', 'value': 'str_to_date(concat(date_format(tgl_masuk, "%%Y-%%m"), "-01"), "%%Y-%%m-%%d")'},]
#     elif delta.days <365:
#         return [{'label': 'Harian', 'value': 'tgl_masuk'},
#                 {'label': 'Mingguan', 'value': 'str_to_date(concat(yearweek(fact_PENGADAAN.tgl_masuk), " Sunday"), "%%X%%V %%W")'},
#                 {'label': 'Bulanan', 'value': 'str_to_date(concat(date_format(tgl_masuk, "%%Y-%%m"), "-01"), "%%Y-%%m-%%d")'},
#                 {'label': 'Quartal', 'value': 'str_to_date(concat(year(fact_PENGADAAN.tgl_masuk), "-", ((quarter(fact_PENGADAAN.tgl_masuk) * 3) - 2), "-01"), "%%Y-%%m-%%d")'},]
#     elif delta.days <730:
#         return [{'label': 'Harian', 'value': 'tgl_masuk'},
#                 {'label': 'Mingguan', 'value': 'str_to_date(concat(yearweek(fact_PENGADAAN.tgl_masuk), " Sunday"), "%%X%%V %%W")'},
#                 {'label': 'Bulanan', 'value': 'str_to_date(concat(date_format(tgl_masuk, "%%Y-%%m"), "-01"), "%%Y-%%m-%%d")'},
#                 {'label': 'Quartal', 'value': 'str_to_date(concat(year(fact_PENGADAAN.tgl_masuk), "-", ((quarter(fact_PENGADAAN.tgl_masuk) * 3) - 2), "-01"), "%%Y-%%m-%%d")'},
#                 {'label': 'Semester', 'value': frekWaktu[4]},]
#     else:
#         return [{'label': 'Harian', 'value': 'tgl_masuk'},
#                 {'label': 'Mingguan', 'value': 'str_to_date(concat(yearweek(fact_PENGADAAN.tgl_masuk), " Sunday"), "%%X%%V %%W")'},
#                 {'label': 'Bulanan', 'value': 'str_to_date(concat(date_format(tgl_masuk, "%%Y-%%m"), "-01"), "%%Y-%%m-%%d")'},
#                 {'label': 'Quartal', 'value': 'str_to_date(concat(year(fact_PENGADAAN.tgl_masuk), "-", ((quarter(fact_PENGADAAN.tgl_masuk) * 3) - 2), "-01"), "%%Y-%%m-%%d")'},
#                 {'label': 'Semester', 'value': frekWaktu[4]},
#                 {'label': 'Tahunan', 'value': 'makedate(YEAR(tgl_masuk),1)'},]
#
# @app.callback(
#     Output('div-stripOrder', 'style'),
#     Output('div-kategoriOrder', 'style'),
#     Input('pengukuranOrder', 'value')
# )
# def change_stateDeep(ukur):
#     if ukur=='Kategori':
#         return {'width': '75%','color':'black','display':'none'}, {'width': '75%','color':'black','display':'block'}
#     if ukur=='Lini':
#         return {'width': '75%','color':'black','display':'block'}, {'width': '75%','color':'black','display':'none'}
#
# @app.callback(
#     Output('filter-stripOrder', 'value'),
#     Output('filter-kategoriOrder', 'value'),
#     Input('pengukuranOrder', 'value')
# )
# def change_valueDeep(ukur):
#     if ukur=='Kategori':
#         return [],[]
#     if ukur=='Lini':
#         return [],[]
#
# #PIE_ORDER
# @app.callback(
#     Output('percent-order', 'figure'),
#     Output('jmlTot', 'children'),
#     Output('jmlTepat', 'children'),
#     Output('jmlTelat', 'children'),
#     Input('filter-tokoOrder', 'value'),
#     Input('filter-supplierOrder', 'value'),
#     Input('filter-stripOrder', 'value'),
#     Input('filter-kategoriOrder', 'value'),
#     Input('dateOrder', 'start_date'),
#     Input('dateOrder', 'end_date'),
# )
# def update_percentOrder(toko, supply, strip, kategori, startDate, endDate):
#     col_toko = tokoAll
#     col_supplier = supplyAll
#     col_kategori = dd['kel_jns'].dropna().unique()
#     col_kode_strip = stripAll
#     df_percentOrder = pd.read_sql('select count(distinct no_faktur) as jml_nota, order_ontime '
#                               'from fact_PENGADAAN '
#                               'inner join dim_STRIP on fact_PENGADAAN.strip_key = dim_STRIP.strip_key '
#                               'inner join dim_SUPPLIERR on fact_PENGADAAN.supplier_key = dim_SUPPLIERR.supplier_key '
#                               'inner join dim_WAKTU on fact_PENGADAAN.tgl_masuk = dim_WAKTU.tanggal '
#                               'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
#                               'where tgl_masuk between %(startDate)s and %(endDate)s '
#                               'and tk.nama_toko in %(toko)s '
#                               'and dim_SUPPLIERR.kode_supplier in %(supply)s '
#                               'and dim_STRIP.kel_jns in %(kel_jns)s '
#                               'and dim_STRIP.kode_strip in %(strip)s '
#                               'group by order_ontime',conn,
#                               params = {'toko': tuple(toko) if len(toko) != 0 or None else tuple(col_toko),
#                                         'supply': tuple(supply) if len(supply) != 0 else tuple(col_supplier),
#                                         'kel_jns': tuple(kategori) if len(kategori) != 0 else tuple(col_kategori),
#                                         'strip': tuple(strip) if len(strip) != 0 else tuple(col_kode_strip),
#                                         'startDate': startDate,
#                                         'endDate': endDate,})
#     tepat = df_percentOrder.loc[(df_percentOrder["order_ontime"] == 'TEPAT'), ('jml_nota')].agg({'jml_nota': np.sum})
#     telat = df_percentOrder.loc[(df_percentOrder["order_ontime"] != 'TEPAT'), ('jml_nota')].agg({'jml_nota': np.sum})
#     angka = tepat + telat
#     txtTot = '' + f"{angka.iloc[-1]:,.0f}"
#     txtTepat = '' + f"{tepat.iloc[-1]:,.0f}"
#     txtTelat = '' + f"{telat.iloc[-1]:,.0f}"
#     fig = go.Figure(data=[go.Pie(labels=df_percentOrder['order_ontime'], values=df_percentOrder['jml_nota'], hole=.4)])
#     fig.update_layout(
#         annotations=[dict(text=f"{angka.iloc[-1]:,.0f}", showarrow=False, font_size=15)]
#     )
#     return fig, txtTot, txtTepat, txtTelat
#
# #BAR_JMLORDER
# @app.callback(
#     Output('sum-order', 'figure'),
#     Input('filter-tokoOrder', 'value'),
#     Input('filter-supplierOrder', 'value'),
#     Input('filter-stripOrder', 'value'),
#     Input('filter-kategoriOrder', 'value'),
#     Input('dateOrder', 'start_date'),
#     Input('dateOrder', 'end_date'),
# )
# def update_SumOrder(toko, supply, strip, kategori, startDate, endDate):
#     col_toko = tokoAll
#     col_supplier = supplyAll
#     col_kategori = dd['kel_jns'].dropna().unique()
#     col_kode_strip = stripAll
#     df_sumOrder = pd.read_sql('select count(distinct no_faktur) as jml_nota, order_ontime, tk.nama_toko as nama_toko '
#                               'from fact_PENGADAAN '
#                               'inner join dim_STRIP on fact_PENGADAAN.strip_key = dim_STRIP.strip_key '
#                               'inner join dim_SUPPLIERR on fact_PENGADAAN.supplier_key = dim_SUPPLIERR.supplier_key '
#                               'inner join dim_WAKTU on fact_PENGADAAN.tgl_masuk = dim_WAKTU.tanggal '
#                               'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
#                               'where tgl_masuk between %(startDate)s and %(endDate)s '
#                               'and tk.nama_toko in %(toko)s '
#                               'and dim_SUPPLIERR.kode_supplier in %(supply)s '
#                               'and dim_STRIP.kel_jns in %(kel_jns)s '
#                               'and dim_STRIP.kode_strip in %(strip)s '
#                               'group by order_ontime, nama_toko',conn,
#                               params = {'toko': tuple(toko) if len(toko) != 0 or None else tuple(col_toko),
#                                         'supply': tuple(supply) if len(supply) != 0 else tuple(col_supplier),
#                                         'kel_jns': tuple(kategori) if len(kategori) != 0 else tuple(col_kategori),
#                                         'strip': tuple(strip) if len(strip) != 0 else tuple(col_kode_strip),
#                                         'startDate': startDate,
#                                         'endDate': endDate,})
#     fig = px.bar(df_sumOrder, x=df_sumOrder['nama_toko'], y=df_sumOrder['jml_nota'], color=df_sumOrder['order_ontime'])
#     return fig
#
# #RATA2_ORDER
# @app.callback(
#     Output('rate-order', 'figure'),
#     Input('radio-rasio', 'value'),
#     Input('filter-tokoOrder', 'value'),
#     Input('filter-supplierOrder', 'value'),
#     Input('filter-stripOrder', 'value'),
#     Input('filter-kategoriOrder', 'value'),
#     Input('dateOrder', 'start_date'),
#     Input('dateOrder', 'end_date'),
#     Input('filter-waktuOrder', 'value'),
# )
# def update_RateRasioOrder(radio_rasio, toko, supply, strip, kategori, startDate, endDate, filterDate):
#     col_toko = tokoAll
#     col_supplier = supplyAll
#     col_kategori = dd['kel_jns'].dropna().unique()
#     col_kode_strip = stripAll
#     rate_all = pd.read_sql('select y.tanggal, x.total_tepat/y.total as "avg" from '
#                 '(select kel_jns, {tgl} as "tanggal", '
#                 'count(distinct no_faktur) as "total_tepat" from fact_PENGADAAN '
#                 'inner join dim_STRIP ds on fact_PENGADAAN.strip_key = ds.strip_key '
#                 'inner join dim_SUPPLIERR d on fact_PENGADAAN.supplier_key = d.supplier_key '
#                 'inner join dim_WAKTU dw on fact_PENGADAAN.tgl_masuk = dw.tanggal '
#                 'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
#                 'where tgl_masuk between %(startDate)s and %(endDate)s and order_ontime = "TEPAT" '
#                 'and tk.nama_toko in %(toko)s '
#                 'and d.kode_supplier in %(supply)s '
#                 'and ds.kel_jns in %(kel_jns)s '
#                 'and ds.kode_strip in %(strip)s group by tanggal) x, '
#                 '(select kel_jns, {tgl} as "tanggal", '
#                 'count(distinct no_faktur) as "total" from fact_PENGADAAN '
#                 'inner join dim_STRIP ds on fact_PENGADAAN.strip_key = ds.strip_key '
#                 'inner join dim_SUPPLIERR d on fact_PENGADAAN.supplier_key = d.supplier_key '
#                 'inner join dim_WAKTU dw on fact_PENGADAAN.tgl_masuk = dw.tanggal '
#                 'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
#                 'where tgl_masuk between %(startDate)s and %(endDate)s '
#                 'and tk.nama_toko in %(toko)s '
#                 'and d.kode_supplier in %(supply)s '
#                 'and ds.kel_jns in %(kel_jns)s '
#                 'and ds.kode_strip in %(strip)s group by tanggal) y '
#                 'where x.tanggal=y.tanggal ORDER by x.tanggal'.format(tgl=filterDate), conn,
#                 params={'toko': tuple(toko) if len(toko) != 0 else tuple(col_toko),
#                         'supply': tuple(supply) if len(supply) != 0 else tuple(col_supplier),
#                         'kel_jns': tuple(kategori) if len(kategori) != 0 else tuple(col_kategori),
#                         'strip': tuple(strip) if len(strip) != 0 else tuple(col_kode_strip),
#                         'startDate': startDate,
#                         'endDate': endDate,})
#     df_rate = pd.read_sql('select x.{radio},y.tanggal, x.total_tepat/y.total as "avg" from '
#                            '(select {radio}, {tgl} as "tanggal", '
#                            'count(distinct no_faktur) as "total_tepat" from fact_PENGADAAN '
#                            'inner join dim_STRIP ds on fact_PENGADAAN.strip_key = ds.strip_key '
#                            'inner join dim_SUPPLIERR d on fact_PENGADAAN.supplier_key = d.supplier_key '
#                            'inner join dim_WAKTU dw on fact_PENGADAAN.tgl_masuk = dw.tanggal '
#                            'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
#                            'where tgl_masuk between %(startDate)s and %(endDate)s and order_ontime = "TEPAT" '
#                            'and tk.nama_toko in %(toko)s '
#                            'and d.kode_supplier in %(supply)s '
#                            'and ds.kel_jns in %(kel_jns)s '
#                            'and ds.kode_strip in %(strip)s group by tanggal, {radio} order by tanggal) x, '
#                            '(select {radio}, {tgl} as "tanggal", '
#                            'count(distinct no_faktur) as "total" from fact_PENGADAAN '
#                            'inner join dim_STRIP ds on fact_PENGADAAN.strip_key = ds.strip_key '
#                            'inner join dim_SUPPLIERR d on fact_PENGADAAN.supplier_key = d.supplier_key '
#                            'inner join dim_WAKTU dw on fact_PENGADAAN.tgl_masuk = dw.tanggal '
#                            'inner join dim_TOKO tk on fact_PENGADAAN.kode_toko = tk.kode_toko '
#                            'where tgl_masuk between %(startDate)s and %(endDate)s '
#                            'and tk.nama_toko in %(toko)s '
#                            'and d.kode_supplier in %(supply)s '
#                            'and ds.kel_jns in %(kel_jns)s '
#                            'and ds.kode_strip in %(strip)s group by tanggal, {radio} order by tanggal) y '
#                            'where x.tanggal=y.tanggal and x.{radio}=y.{radio}'.format(radio=radio_rasio,tgl=filterDate), conn,
#                            params={'toko': tuple(toko) if len(toko)!=0 else tuple(col_toko),
#                                    'supply':tuple(supply) if len(supply) !=0 else tuple(col_supplier),
#                                    'kel_jns': tuple(kategori) if len(kategori) != 0 else tuple(col_kategori),
#                                    'strip':tuple(strip) if len(strip) != 0 else tuple(col_kode_strip),
#                                    'startDate': startDate,
#                                    'endDate': endDate,})
#     if(len(df_rate['tanggal'])!=0 or len(df_rate['avg'])!=0):
#         fig = px.bar(df_rate, x=df_rate['tanggal'], y=df_rate['avg'], color=df_rate[radio_rasio])
#         fig.update_layout(xaxis=dict(tickvals=df_rate['tanggal'].unique()))
#         # fig = go.Figure(
#         #     data=[
#         #         go.Bar(name='01', x=df_toko['tanggal'],y=df_toko.loc[df_toko['kode_toko'] == '01', ('avg')].values.tolist()),
#         #         go.Bar(name='05', x=df_toko['tanggal'],y=df_toko.loc[df_toko['kode_toko'] == '05', ('avg')].values.tolist())
#         #     ], layout=go.Layout(showlegend=True, barmode='stack'))
#         fig.add_scatter(name='all', x=rate_all['tanggal'], y=rate_all['avg'], marker={'color': 'rgb(0,0,90)'})
#         # fig.update_traces(mode='lines+markers')
#         return fig
#     else:
#         fig = go.Figure().add_annotation(x=2.5, y=2,text="Tidak Ada Data yang Ditampilkan",font=dict(family="sans serif",size=25,color="crimson"),showarrow=False,yshift=10)
#         return fig
#
# if __name__ == '__main__':app.run_server(debug=True)
