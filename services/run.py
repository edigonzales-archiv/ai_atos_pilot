#!venv/bin/python
from flask import Flask
from flask import g
from flask import Response
from flask import request
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

TIMEZONE = timezone('Europe/Amsterdam')

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
    """ Creates the service feed response xml. It reads the information
    from a sqlite database.
    The following implementation allows only one service feed from the sqlite
    database. You would need to adjust the sql queries (and it would require
    also some parameters in the route).
    """
    app.logger.debug('Entering service_feed_xml() method.')

    # We need to know the date/time of the last modification of *any* data.
    max_updated = datetime.datetime.strptime("1900-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")

    # 1) Get data for service feed.
    app.logger.debug('Get service feed information from database.')

    query = "SELECT * FROM service_feed LIMIT 1;"

    sf_pkuid = None
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
        app.logger.error('No service feed found in database.')
        abort(404)

    # 2) Get all entries belonging to the previously requested service feed.
    app.logger.debug('Get all service feed entries from database belonging to \
                      previously requested service feed.')

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
        sfe_item['updated'] = TIMEZONE.localize(updated).isoformat('T')

        sfe_item['bbox'] = str(service_feed_entry['x_min']) + " " + str(service_feed_entry['y_min']) + " " + \
                       str(service_feed_entry['x_max']) + " " + str(service_feed_entry['y_max'])

        # Get all CRS that are available for datasets belonging to this
        # service feed entry.
        app.logger.debug('Get all available CRS for service feed entry.')

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
        app.logger.debug('Find out newest update of service veed entry.')

        if updated > max_updated:
            max_updated = updated
            max_updated_iso = TIMEZONE.localize(updated).isoformat('T')

    response = make_response(render_template('servicefeed.xml', title = title,
                    subtitle = subtitle, self_link = self_link,
                    describedby_link = describedby_link,
                    search_link = search_link, rights = rights,
                    max_updated = max_updated_iso, items = sfe_items))
    response.headers['Content-Type'] = 'text/xml; charset=utf-8'
    return response


@app.route('/atos/dls/<dataset_id>', methods=['GET'])
def dataset_feed_xml(dataset_id):
    """ Creates the dataset feed response xml. It reads the information
    from a sqlite database.
    It uses 'identifier_code' as dataset_id / parameter. This works only if we
    suppose that 'identifier_code' is unique at this endpoint (database).
    """
    app.logger.debug('Entering dataset_feed_xml() method.')

    dataset_id = dataset_id.split(".")[0]
    app.logger.debug('dataset_id: %s', str(dataset_id))

    # We need to know the date/time of the last modification of *any* data.
    max_updated = datetime.datetime.strptime("1900-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")

    # 1) Get data for dataset feed.
    app.logger.debug('Get dataset feed information from database.')

    query = "SELECT df.pkuid, df.title, df.subtitle, df.rights \
             FROM service_feed_entry as sfe, dataset_feed as df \
             WHERE sfe.identifier_code = ? \
             AND sfe.pkuid = df.sfe_id;"
    args = (dataset_id,)

    df_pkuid = None
    for dataset_feed in query_db(query, args):
        df_pkuid = dataset_feed['pkuid']
        title = dataset_feed['title']
        subtitle = dataset_feed['subtitle']
        rights = dataset_feed['rights']

    if not df_pkuid:
        app.logger.error('No dataset feed found in database: %s', str(dataset_id))
        abort(404)

    # 2) Get describedby_links. Which are references to the MGDM ili models.
    app.logger.debug('Get describedby_links (MGDM models) information from database.')

    query = "SELECT DISTINCT dfm.describedby_link \
             FROM service_feed_entry as sfe, dataset_feed as df, \
                  dataset_feed_models as dfm \
             WHERE sfe.identifier_code = ? \
             AND sfe.pkuid = df.sfe_id \
             AND df.pkuid = dfm.df_id;"
    args = (dataset_id,)

    mdl_items = []
    for model in query_db(query, args):
        mdl_item = {}
        mdl_item['describedby_link'] = model['describedby_link']

    mdl_items.append(mdl_item)

    # 3) Now get the information for dataset feed entries.
    app.logger.debug('Get dataset feed entries information from database.')

    query = "SELECT df.title || ' ' ||  dfe.srs_auth || ':' || dfe.srs_code || \
                    ' (' || dfe.format_txt || ')' as title  , dfe.alternate_link, \
                    dfe.summary, dfe.format_mime, dfe.format_txt, dfe.srs_auth, \
                    dfe.srs_code, dfe.srs_txt, dfe.updated, sfe.x_min,  \
                    sfe.y_min, sfe.x_max, sfe.y_max \
             FROM service_feed_entry as sfe, dataset_feed as df, \
                  dataset_feed_entry as dfe \
             WHERE sfe.identifier_code = ? \
             AND sfe.pkuid = df.sfe_id \
             AND df.pkuid = dfe.df_id;"
    args = (dataset_id,)

    dfe_items = []
    for dataset_feed_entry in query_db(query, args):
        dfe_item = {}
        dfe_item['title'] = dataset_feed_entry['title']
        dfe_item['alternate_link'] = dataset_feed_entry['alternate_link']
        dfe_item['summary'] = dataset_feed_entry['summary']
        dfe_item['format_mime'] = dataset_feed_entry['format_mime']
        dfe_item['format_txt'] = dataset_feed_entry['format_txt']
        dfe_item['srs_auth'] = dataset_feed_entry['srs_auth']
        dfe_item['srs_code'] = dataset_feed_entry['srs_code']
        dfe_item['srs_txt'] = dataset_feed_entry['srs_txt']

        updated = datetime.datetime.strptime(dataset_feed_entry['updated'], '%Y-%m-%d %H:%M:%S')
        dfe_item['updated'] = TIMEZONE.localize(updated).isoformat('T')

        dfe_item['bbox'] = str(dataset_feed_entry['x_min']) + " " + str(dataset_feed_entry['y_min']) + " " + \
                       str(dataset_feed_entry['x_max']) + " " + str(dataset_feed_entry['y_max'])

        dfe_items.append(dfe_item)

        # We need to find out the newest update of a service feed entry.
        app.logger.debug('Find out newest update of service veed entry.')

        if updated > max_updated:
            max_updated = updated
            max_updated_iso = TIMEZONE.localize(updated).isoformat('T')

    # 4) Assign remaining variables.
    service_link = SERVICE_URL

    response = make_response(render_template('datasetfeed.xml', title = title,
                    subtitle = subtitle, service_link = service_link, \
                    identifier_code = dataset_id, rights = rights, \
                    mdl_items = mdl_items, max_updated = max_updated_iso, \
                    items = dfe_items))
    response.headers['Content-Type'] = 'text/xml; charset=utf-8'
    return response


@app.route('/atos/search/opensearchdescription.xml', methods=['GET'])
def opensearchdescription_xml():
    """ Creates the opensearch description response xml.
    Language is hardcoded to "de".
    Contact/LongName is hardcoded.
    ShortName/Description is hardcoded (= title/subtitle from service feed)
    """
    app.logger.debug('Entering opensearchdescription_xml() method.')

    # 1) Collect all mime types for this download service.
    # Keep in mind that this query works only for this implementation.
    # -> only one service feed in the database possible.
    app.logger.debug('Get mime types for this download service from database.')

    query = "SELECT DISTINCT dfe.format_mime \
             FROM service_feed_entry as sfe, dataset_feed as df, \
                  dataset_feed_entry as dfe \
             WHERE sfe.pkuid = df.sfe_id \
             AND df.pkuid = dfe.df_id;"

    mime_type_items = []
    for mime_type in query_db(query):
        mime_type_items.append(mime_type['format_mime'])

    # 2) We write every available dataset in the Query-stuff. Corresponding
    # to Inspire-TC there is only one per identifier_code/identifier_namespace.
    # But e.g. Weichand and Pasquale also provide all crs dataset combination.
    app.logger.debug('Get all datasets for opensearch query.')

    query = "SELECT sfe.identifier_code, sfe.identifier_namespace, df.title, \
                    dfe.format_mime, dfe.format_txt, dfe.srs_auth, \
                    dfe.srs_code, dfe.srs_txt \
             FROM service_feed_entry as sfe, dataset_feed as df, \
                  dataset_feed_entry as dfe \
             WHERE sfe.pkuid = df.sfe_id \
             AND df.pkuid = dfe.df_id;"

    ex_items = []
    for examples in query_db(query):
        ex_item = {}
        ex_item['identifier_code'] = examples['identifier_code']
        ex_item['identifier_namespace'] = examples['identifier_namespace']
        ex_item['title'] = examples['title']
        ex_item['format_mime'] = examples['format_mime']
        ex_item['srs_auth'] = examples['srs_auth']
        ex_item['srs_code'] = examples['srs_code']
        ex_items.append(ex_item)

    # 3) Assign remaining variables.
    search_link = SEARCH_URL

    response = make_response(render_template('opensearchdescription.xml', \
                    search_link = search_link, \
                    ex_items = ex_items, mime_type_items = mime_type_items))
    response.headers['Content-Type'] = 'text/xml; charset=utf-8'
    return response

@app.route('/atos/search', methods=['GET'])
def search():
    """ Handles the 'service part' of download service.

    Requests:
    DescribeSpatialDataSet
    GetSpatialDataSet
    """
    app.logger.debug('Entering search() method.')

    params_len = len(request.args)

    # Abort if there are no parameters at all.
    if params_len == 0:
        app.logger.error('No query string found.')
        abort(404)

    # What is the client requesting?
    # lowercase key and value of query string.
    request_dict = { k.lower():v.lower() for k, v in request.args.items() }
    request_param = request_dict.get('request')

    # Service feed.
    if request_param == "getdownloadservicemetadata":
        app.logger.debug('getdownloadservicemetadata')
        return service_feed_xml()

    # Dataset description -> redirect to dataset feed.
    # We take a shurtcut: Just redirect to dataset_feed_xml(identifier_code).
    # This is not super smart but we still assume that 'identifier_code' is
    # unique in our endpoint (service feed).
    # We do not check if 'identifier_code' is available. We do this in the
    # database_feed_xml() method.
    # We should do this here since we also request the identifier_namespace...
    # No identifier_namespace has no impact and can be anything.
    elif request_param == "describespatialdataset":
        app.logger.debug('describespatialdataset')
        identifier_code = request.args.get('spatial_dataset_identifier_code', '')
        identifier_namespace = request.args.get('spatial_dataset_identifier_namespace', '')
        # language and q are ignored

        if not identifier_code:
            app.logger.error('No identifier_code found in query string.')
            abort(404)
        if not identifier_namespace:
            app.logger.error('No identifier_namespace found in query string.')
            abort(404)

        return dataset_feed_xml(identifier_code)

    # Dataset download.
    elif request_param == "getspatialdataset":
        app.logger.debug('getspatialdataset')
        identifier_code = request.args.get('spatial_dataset_identifier_code', '')
        identifier_namespace = request.args.get('spatial_dataset_identifier_namespace', '')
        mediatype = request.args.get('mediatype', '')
        crs = request.args.get('crs', '')
        # language and q are ignored

        if not identifier_code:
            app.logger.error('No identifier_code found in query string.')
            abort(404)
        if not identifier_namespace:
            app.logger.error('No identifier_namespace found in query string.')
            abort(404)
        if not mediatype:
            app.logger.error('No mediatype found in query string.')
            abort(404)
        if not crs:
            app.logger.error('No crs found in query string.')
            abort(404)

        # Get the srs_code.
        # srs_auth is ignored.
        srs_code = crs.split("/")[-1]

        # Query the database.
        # There is no error handling at the moment.
        # What happens if we found more than one dataset? haha limit 1
        query = "SELECT dfe.alternate_link \
                 FROM service_feed_entry as sfe, dataset_feed as df, \
                      dataset_feed_entry as dfe \
                 WHERE sfe.pkuid = df.sfe_id \
                 AND df.pkuid = dfe.df_id \
                 AND sfe.identifier_code = ? \
                 AND sfe.identifier_namespace = ? \
                 AND dfe.format_mime = ? \
                 AND srs_code = ? \
                 LIMIT 1;"
        args = (identifier_code, identifier_namespace, mediatype, srs_code)

        dataset_url = None
        for datasets in query_db(query, args):
            dataset_url = datasets['alternate_link']

        if not dataset_url:
            app.logger.error('Dataset not found in database: %s', identifier_code)
            abort(404)

        return redirect(dataset_url)

    else:
        app.logger.error('missing query string')
        abort(404)

# Example requests
# http://localhost:5000/atos/search?request=DescribeSpatialDataset&spatial_dataset_identifier_code=788f4376-a625-4c0a-8704-458aa59bff79&spatial_dataset_identifier_namespace=http://www.geodienste.ch
# http://localhost:5000/atos/search?request=GetSpatialdataSet&spatial_dataset_identifier_code=788f4376-a625-4c0a-8704-458aa59bff79&spatial_dataset_identifier_namespace=http://www.geodienste.ch&mediatype=application/gml%2bxml;version=3.2&crs=http://www.opengis.net/def/crs/EPSG/0/21781

# Database stuff:
# http://flask.pocoo.org/docs/0.10/patterns/sqlite3/
# http://stackoverflow.com/questions/16311974/connect-to-a-database-in-flask-which-approach-is-better
# one request = one connection?

@app.before_request
def before_request():
    """ Creates a connection to the database before anything else is done.
    It always creates one!
    """
    g.db = connect_db()


def connect_db():
    #conn = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def query_db(query, args=(), one=False):
    """ Performes sql query.
    Use args for preventing sql injections.
    """
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.teardown_request
def teardown_request(exception):
    """ Closes the database connection."""
    if hasattr(g, 'db'):
        g.db.close()


if __name__ == "__main__":
    #handler = RotatingFileHandler('atomfeed_opensearch.log', maxBytes=1048576, backupCount=3)
    #handler.setLevel(logging.DEBUG)
    #app.logger.addHandler(handler)
    app.run(debug=True)
