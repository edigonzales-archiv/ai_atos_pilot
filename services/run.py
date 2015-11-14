#!venv/bin/python
from flask import Flask
from flask import g
from flask import Response
from flask import render_template
from flask import make_response
from flask import abort
from flask import redirect
from pytz import timezone
from datetime import datetime, time

#from logging.handlers import RotatingFileHandler
#from logging import Formatter
import logging
import sqlite3
import datetime

#SERVICE_URL = "http://www.geodienste.ch/services/atos"
#SEARCH_URL = "http://www.geodienste.ch/services/atos/search"
SERVICE_URL = "http://127.0.0.1:5000/atos/dls"
SEARCH_URL = "http://127.0.0.1:5000/atos/search"

DATABASE = "/home/stefan/Projekte/ai_atos_pilot/metadb/metadb.sqlite"

app = Flask(__name__)

@app.route("/")
def main():
    return "Welcome!"


@app.route('/atos/dls/service.xml', methods=['GET'])
def service_feed_xml():
    app.logger.debug('Entering service_feed_xml() method.')

    # The following implementation allows only one service feed from
    # the meta database.
    # You would need to adjust the sql queries (and would require also some
    # parameters in the route).

    # We need to know the date/time of the last modification of *any* data.
    my_timezone = timezone('Europe/Amsterdam')
    max_updated = datetime.datetime.strptime("1900-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")

    # 1) Get data for service feed.
    query = "SELECT * FROM service_feed LIMIT 1;"

    for service_feed in query_db(query):
        sf_pkuid = service_feed['pkuid']
        title = service_feed['title']
        subtitle = service_feed['subtitle']
        describedby_link = service_feed['describedby_link']
        #search_link = service_feed['search_link']
        search_link = SEARCH_URL
        self_link = SERVICE_URL
        rights = service_feed['rights']

    if not sf_pkuid:
        app.logger.error('No service feed found in metadb.')
        abort(404)

    # 2) Get all entries belonging to the previously requested service feed.
    query = "SELECT * FROM service_feed_entry WHERE sf_id = ?"
    args = (sf_pkuid,)

    sfe_items = []
    for service_feed_entry in query_db(query, args):
        sfe_pkuid = service_feed_entry['pkuid']
        sfe_item =  {}
        sfe_item['identifier_code'] = service_feed_entry['identifier_code']
        sfe_item['identifier_namespace'] = service_feed_entry['identifier_namespace']
        sfe_item['title'] = service_feed_entry['title']
        sfe_item['subtitle'] = service_feed_entry['subtitle']
        sfe_item['summary'] = service_feed_entry['summary']
        sfe_item['describedby_link'] = service_feed_entry['describedby_link']
        sfe_item['rights'] = service_feed_entry['rights']

        # sqlite3.PARSE_DECLTYPES does not work.
        # Convert string to date object manually.
        updated = datetime.datetime.strptime(service_feed_entry['updated'], '%Y-%m-%d %H:%M:%S')
        sfe_item['updated'] = my_timezone.localize(updated).isoformat('T')

        sfe_item['bbox'] = str(service_feed_entry['x_min']) + " " + str(service_feed_entry['y_min']) + " " + \
                       str(service_feed_entry['x_max']) + " " + str(service_feed_entry['y_max'])

        # Get all CRS that are available for datasets belonging to this
        # service feed entry.
        query = "SELECT DISTINCT sfe.pkuid, df.pkuid, srs_auth, srs_code, srs_txt \
                 FROM service_feed_entry as sfe, dataset_feed as df, \
                      dataset_feed_entry as dfe \
                 WHERE sfe.pkuid = df.sfe_id \
                 AND df.pkuid = dfe.df_id \
                 AND sfe.pkuid = ?"
        args = (sfe_pkuid,)

        crs_items = []
        for coordsys in query_db(query, args):
            crs_item = {}
            crs_item['srs_auth'] = coordsys['srs_auth']
            crs_item['srs_code'] = coordsys['srs_code']
            crs_item['srs_txt'] = coordsys['srs_txt']
            crs_items.append(crs_item)

        sfe_item['crs'] = crs_items

        sfe_items.append(sfe_item)

        # We need to find out the newest update of a service feed entry.
        if updated > max_updated:
            max_updated = updated
            max_updated_iso = my_timezone.localize(updated).isoformat('T')

    response = make_response(render_template('servicefeed.xml', title = title,
                    subtitle = subtitle, self_link = self_link,
                    describedby_link = describedby_link,
                    search_link = search_link, rights = rights,
                    max_updated = max_updated_iso, items = sfe_items))
    response.headers['Content-Type'] = 'text/xml; charset=utf-8'
    return response


@app.route('/atos/dls/<dataset_id>', methods=['GET'])
def dataset_feed_xml(dataset_id):
    app.logger.debug('Entering dataset_feed_xml() method.')

    dataset_id = dataset_id.split(".")[0]
    app.logger.debug('dataset_id: %s', str(dataset_id))


    # Avoid SQL injections:
    # http://bobby-tables.com/python.html
    # https://docs.python.org/2/library/sqlite3.html


    return "dataset feed"



# Database stuff:
# http://flask.pocoo.org/docs/0.10/patterns/sqlite3/
# http://stackoverflow.com/questions/16311974/connect-to-a-database-in-flask-which-approach-is-better
# one request = one connection?

def connect_db():
    #conn = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


if __name__ == "__main__":
    #handler = RotatingFileHandler('atomfeed_opensearch.log', maxBytes=1048576, backupCount=3)
    #handler.setLevel(logging.DEBUG)
    #app.logger.addHandler(handler)
    app.run(debug=True)
