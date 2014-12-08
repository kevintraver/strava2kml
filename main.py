from flask import Flask, render_template, request, url_for, send_file
import requests
from lxml import html
import simplekml
import StringIO

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        segment_id = request.form['segmentId']
        url = 'http://www.strava.com/stream/segments/' + segment_id + '.json'
        segment_title = html.fromstring(requests.get('http://www.strava.com/segments/' + segment_id).text).xpath('//title')[0].text
        json = requests.get(url).json()
        coordinates = json['latlng']
        kml = simplekml.Kml()
        kml.newlinestring(name=segment_title, coords=[tuple(coordinate)[::-1] for coordinate in coordinates])
        strIO = StringIO.StringIO()
        strIO.write(str(kml.kml()))
        strIO.seek(0)
        return send_file(strIO, attachment_filename=segment_title + ".kml", as_attachment=True)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()
