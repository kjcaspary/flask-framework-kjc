import requests
import bokeh.plotting.figure
import bokeh
import pandas
import datetime
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def stock_plot(symbol='GOOG',yr=2017,mo=11,day=22):

#    symbols = ['GOOG']
#    symbol = symbols[0]
    dt = datetime.date(yr,mo,day)
    day = datetime.timedelta(1)
    dates = '%2C'.join([str(dt - day*x) for x in range(30)])
    #print dates[0:]
    
    
    r = requests.get('http://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker='+symbol+'&date='+dates+'&qopts.columns=ticker,date,close&api_key=TSuUhExFF7FcVbQ_xkxp')
    
    names = [x['name'] for x in r.json()['datatable']['columns']]
    df = pandas.DataFrame(r.json()['datatable']['data'], columns = names)
    df['date'] = pandas.to_datetime(df['date'])
    
    
    p = bokeh.plotting.figure()
    p.line(df['date'],df['close'])
    bokeh.plotting.show(p)
    return p

@app.route('/')
def index():
	# Determine the selected feature
    sym='GOOG'
    yr=2017
    mo=11
    day=22
	# Create the plot
    plot = stock_plot(sym,yr,mo,day)
		
	# Embed plot into HTML via Flask Render
    script, div = bokeh.embed.components(plot)
    return render_template("index.html", script=script, div=div)

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run()
