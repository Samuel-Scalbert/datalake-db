from flask import Flask, render_template
from pyArango.connection import Connection
from Utils.db import insert_json_db
app = Flask(__name__,template_folder='templates',static_folder='static')

#app.config['ARANGO_HOST'] = 'arangodb'
app.config['ARANGO_HOST'] = 'localhost'
app.config['ARANGO_PORT'] = 8529
app.config['ARANGO_DB'] = 'Datalake-DB'
app.config['ARANGO_USERNAME'] = 'root'
app.config['ARANGO_PASSWORD'] = 'root'

def init_db():
    global db
    db = Connection(
        arangoURL='http://{host}:{port}'.format(
            host=app.config['ARANGO_HOST'],
            port=app.config['ARANGO_PORT']
        ),
        username=app.config['ARANGO_USERNAME'],
        password=app.config['ARANGO_PASSWORD']
    )
    if not db.hasDatabase('Datalake-DB'):
        db.createDatabase('Datalake-DB')
    db = Connection(
        arangoURL='http://{host}:{port}'.format(
            host=app.config['ARANGO_HOST'],
            port=app.config['ARANGO_PORT']
        ),
        username=app.config['ARANGO_USERNAME'],
        password=app.config['ARANGO_PASSWORD']
    )[app.config['ARANGO_DB']]

init_db()  # Call the init_db function to initialize the db variable

insert_json_db('./app/data/json_files/', db)

from app.routes import api_doc_to_mention

@app.route('/')
def home():
    return ""

