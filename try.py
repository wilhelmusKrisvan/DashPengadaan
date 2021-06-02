import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc #trs tgl pake aja ini nya
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
import numpy as np
import plotly.express as px

from datetime import date, datetime
from datetime import timedelta
from dash.dependencies import Input, Output, State

from sqlalchemy import create_engine

connect = 'mysql+pymysql://admindw:admindw@10.10.14.5/amigodw'
conn = create_engine(connect)

test_dict = {'Harian':['tgl_masuk',1],
             'Mingguan':'str_to_date(concat(yearweek(fact_PENGADAAN.tgl_masuk), " Sunday"), "%%X%%V %%W")',
             'Bulanan':'str_to_date(concat(date_format(tgl_masuk, "%%Y-%%m"), "-01"), "%%Y-%%m-%%d")',
             'Quartal':'str_to_date(concat(year(fact_PENGADAAN.tgl_masuk), "-", ((quarter(fact_PENGADAAN.tgl_masuk) * 3) - 2), "-01"), "%%Y-%%m-%%d")',
             'Semester':'concat(year(tgl_masuk)," ",IF(MONTH(tgl_masuk) < 7, "Ganjil", "Genap"))',
             'Tahunan':'makedate(YEAR(tgl_masuk),1)'}
print([(k, test_dict[k]) for k in test_dict])
print(test_dict)
