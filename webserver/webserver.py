from flask import Flask
from flask import render_template
import pymongo
from bson import json_util
import json
import logging

import json
import plotly
import pandas as pd
import numpy as np

app = Flask(__name__)


def generate_datasets(timeframe, datatype, title):

    coll = pymongo.MongoClient().saivasdata.resampled
    tempz = []
    y = []
    x = []
    for curs in coll.find({"timeframe": timeframe, "datatype": datatype}).sort("ts", pymongo.ASCENDING):
        # print(curs)

        col = []
        # sort the list so the dictionaries are sorted according to pressure
        newlist = sorted(curs['divedata'], key=lambda k: -k['pressure(dBAR)'])
        for i in newlist:
            col.append(i[datatype])
            if -i['pressure(dBAR)'] not in y:
                y.append(-i['pressure(dBAR)'])

        tempz.append(col)
        x.append(curs['ts'])
    z = list(map(list, zip(*tempz)))
    y = sorted(y)

    graphs = [
        dict(
            data=[
                dict(
                    z=z,
                    x=x,
                    y=y,
                    type='heatmap'
                ),
            ],
            layout=dict(
                title=title
            )
        )
    ]

    return graphs  # x, y, z  # [go.Heatmap(x=x, y=y, z=z)]


@app.route('/')
def frontpage():
    return render_template('frontpage.html')
    # return 'Gabriel web server'


@app.route('/allgraphs')
def allgraphs():
    ids = []
    graphs = []
    for g in [{'id': 'temp', 'desc': 'temp vs dybde over tid'},
              {'id': 'oxygene', 'desc': 'oksygen vs dybde over tid'},
              {'id': 'salt', 'desc': 'salt vs dybde over tid'},
              {'id': 'fluorescens', 'desc': 'fluorescens vs dybde over tid'},
              {'id': 'turbidity', 'desc': 'turbiditet vs dybde over tid'}, ]:
        graph = generate_datasets('3H', g['id'], g['desc'])
        ids.append(g['id'])
        graphs.append(graph[0])

    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('graphview.html',
                           ids=ids,
                           graphJSON=graphJSON)

    return render_template('graphview.html')


@app.route('/count')
def count():
    coll = pymongo.MongoClient().saivasdata.gabrielraw
    return 'dives {}'.format(coll.find().count())

@app.route('/dives')
def dives():
    coll = pymongo.MongoClient().saivasdata.gabrielraw
    cdives = []
    # get all dives
    divecursor = coll.find().sort('startdatetime', pymongo.DESCENDING).limit(100)
    for dive in divecursor:
        cdives.append(dive)
    return render_template('listdives.html', dives=cdives)

@app.route('/dives')
def divesjson():
    coll = pymongo.MongoClient().saivasdata.gabrielraw
    cdives = []
    # get all dives
    divecursor = coll.find().sort('startdatetime', pymongo.DESCENDING).limit(100)
    for dive in divecursor:
        cdives.append(dive)
    return render_template('listdives.html', dives=cdives)

@app.route('/dives/<diveid>')
def onedive(diveid):
    coll = pymongo.MongoClient().saivasdata.gabrielraw
    searchid = int(diveid)
    dive = coll.find_one({"profilenumber": searchid})
    if dive != None:
        retstring = json.dumps(dive, default=json_util.default)
        return json.dumps(retstring)  # 'dive number {}'.format(dive['_id'])
    else:
        return 'None '

@app.route('/dives/<diveid>.json')
def onedivejson(diveid):
    coll = pymongo.MongoClient().saivasdata.gabrielraw
    searchid = int(diveid)
    dive = coll.find_one({"profilenumber": searchid})
    if dive != None:
        retstring = json.dumps(dive, default=json_util.default)
        return json.dumps(retstring)  # 'dive number {}'.format(dive['_id'])
    else:
        return 'None '

@app.route('/stats')
def stats():
    return render_template('stats.html')

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()
