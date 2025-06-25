from app.app import app, db

@app.route('/api/doc_to_mention/<id_doc>')
def list_software(id_doc):
    query = f'''
            for doc in documents
                filter doc._key == "{id_doc}"
                    for doc_edge in edge_doc_to_software
                        filter doc_edge._from == doc._id
                         let soft_mention = document(doc_edge._to)
                         return soft_mention
            '''
    print(query)
    response = db.AQLQuery(query, rawResults=True, batchSize=2000)
    return list(response)