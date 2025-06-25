from app.app import app, db

@app.route('/api/doc_to_mention/<id_doc>')
def list_software(id_doc):
    query = f'''
        LET list_id_soft = (
          FOR doc IN documents
            FILTER doc._key == "{id_doc}"
            FOR doc_edge IN edge_doc_to_software
              FILTER doc_edge._from == doc._id
              LET soft_mention = DOCUMENT(doc_edge._to)
              RETURN soft_mention
        )
        
        FOR mention IN list_id_soft
          COLLECT normalized = mention.software_name.normalizedForm INTO group
          LET attrs = group[0].mention.documentContextAttributes
          LET filtered_mentions = (
          FOR m IN group[*].mention
            RETURN UNSET(m, "documentContextAttributes")
        )
          LET trueAttrs = (
            FOR key IN ATTRIBUTES(attrs)
              FILTER attrs[key].value == true
              RETURN key
          )
          RETURN {{
            software_name: normalized,
            attributes_document_lvl: trueAttrs,
            mentions: filtered_mentions
          }}

            '''
    response = db.AQLQuery(query, rawResults=True, batchSize=2000)
    return list(response)