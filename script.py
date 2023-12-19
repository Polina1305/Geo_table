from sentence_transformers import SentenceTransformer, util
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
import pandas as pd
from psycopg2 import OperationalError


def create_connection(name, user, password, host, port, database):
    engine = None
    try: 
        DATABASE = {
            'drivername': name,
            'username': user, 
            'password': password, 
            'host': host,
            'port': port,
            'database': database,
            'query': {}
        }

        engine = create_engine(URL(**DATABASE))
        print("Connection to PostgreSQL DB successful")
    except:
        print("The error")
    return engine 


def query_table(engine, model_id):
    query = '''SELECT
                      DISTINCT(city.geonameid),
                      city.name,
                      admin.region,
                      country_info.country
                  FROM
                      cities_reloc as city
                      INNER JOIN admin_codes_ascii as admin on city.code = admin.code
                      INNER JOIN country_info on city.country_code = country_info.country_code
                  '''
    data = pd.read_sql(sql=text(query), con=engine.connect())
    names = data.name.values
    
    model_id = model_id
    labse = SentenceTransformer(model_id)
    embeddings = labse.encode(names)
    embedding = pd.DataFrame({"embedding_values": [embedding.tolist() for embedding in embeddings]})
    data['embedding'] = embedding['embedding_values']
    
    data.to_sql('embeddings_lapse', con=engine.connect(), if_exists='replace')
    
    return names, embeddings, labse

def find_similar_labse(geoname, names, embeddings, model, top_k):
    response = pd.DataFrame(util.semantic_search(query_embeddings= model.encode(geoname), corpus_embeddings=embeddings, top_k=top_k)[0])
    cos_sim = response.assign(name=names[response.corpus_id])
    return  cos_sim

def result_model(cos_sim, engine):
     
    index_list = []    
    for i in cos_sim.values:
        index_list.append(i[0])  
    query_emb = "SELECT index, geonameid, name, region, country FROM embeddings_lapse WHERE index = ANY(:indexes)"
    res_emb = engine.connect().execute(text(query_emb).bindparams(indexes=index_list))
    
    response =  [item for item in res_emb]
    sorted_response = sorted(response, key=lambda x: cos_sim.corpus_id.tolist().index(x[0]))
    result = [] 
    for i, item in enumerate(sorted_response): 
      result.append({ 
        'geonameid': item[1], 
        'name': item[2], 
        'region': item[3], 
        'country': item[4], 
        'cosine_similarity': cos_sim.values[i][1] 
      }) 
    return result
