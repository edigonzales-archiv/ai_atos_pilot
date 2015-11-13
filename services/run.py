#!venv/bin/python
from flask import Flask
from flask import g
#from logging.handlers import RotatingFileHandler
#from logging import Formatter
import logging
import sqlite3

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

    app.logger.debug(g.db)

    # The following implementation allows only one service feed from
    # the meta database.
    # You would need to adjust the sql queries (and I guess also some
    # parameters in the route).

    for service_feed in query_db('SELECT  * FROM  service_feed'):
        print service_feed['title'], 'has the id', service_feed[1]






    return "service feed"

@app.route('/atos/dls/<dataset_id>', methods=['GET'])
def dataset_feed_xml(dataset_id):
    app.logger.debug('Entering dataset_feed_xml() method.')

    dataset_id = dataset_id.split(".")[0]
    app.logger.debug('dataset_id: %s', str(dataset_id))

    return "dataset feed"



# Database stuff
# http://flask.pocoo.org/docs/0.10/patterns/sqlite3/
# http://stackoverflow.com/questions/16311974/connect-to-a-database-in-flask-which-approach-is-better
# One request = one connection?

def connect_db():
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
