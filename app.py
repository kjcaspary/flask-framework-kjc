import requests
import bokeh.plotting.figure
import bokeh
import pandas
from flask import Flask, render_template, request
from boto.s3.connection import S3Connection
import os

app = Flask(__name__)

def stock_plot(symbol='GOOG',yr=2017,mo=11,day=22,plt_thing = 'close'):
    QUANDL_key = S3Connection(os.environ['QUANDL_KEY'])

#    symbols = ['GOOG']
#    symbol = symbols[0]
    dt = pandas.datetime(yr,mo,day).date()
    day = pandas.Timedelta(days=1)
    dates = '%2C'.join([str(dt - day*x) for x in range(30)])
#    print dates[0:]
    things = ','.join(['ticker','date','close','open','high','low'])
    
    r = requests.get('http://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker='+symbol+'&date='+dates+'&qopts.columns='+things+'&api_key='+str(QUANDL_Key['QUANDL_KEY']))
    
    names = [x['name'] for x in r.json()['datatable']['columns']]
    df = pandas.DataFrame(r.json()['datatable']['data'], columns = names)
    df['date'] = pandas.to_datetime(df['date'])
            
#    print df['date']
    p = bokeh.plotting.figure(title=str(symbol),x_axis_type='datetime')
    p.line(df['date'],df[plt_thing],legend = symbol+' ' + plt_thing)
    # Set the x axis label
    p.xaxis.axis_label = 'Date'

    # Set the y axis label
    p.yaxis.axis_label = 'Price'

#    bokeh.plotting.show(p)
    return p

@app.route('/')
def index():
    # Determine the selected feature
    sym = request.args.get("stockticker")
    if sym == None:
        sym = 'GOOG'
    date = request.args.get("stdate")
    if date == None:
        date = pandas.datetime(2018,3,27)
    date = pandas.to_datetime(date).date()
    yr=date.year
    mo=date.month
    day=date.day
    plot_thing = request.args.get("choice")
    print plot_thing
    if plot_thing == None:
        plot_thing = 'close'

    # Create the plot
    plot = stock_plot(sym,yr,mo,day,plot_thing)
    js_resources = bokeh.resources.INLINE.render_js()
    css_resources = bokeh.resources.INLINE.render_css()
        
    # Embed plot into HTML via Flask Render
    script, div = bokeh.embed.components(plot)
    return bokeh.util.string.encode_utf8(render_template("index.html", script=script, div=div,js_resources=js_resources,css_resources=css_resources,
                                         stockticker=sym, stdate=date, choice=plot_thing ))

if __name__ == '__main__':
    app.run(port=33507)