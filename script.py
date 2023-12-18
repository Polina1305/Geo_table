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
    except :
        print("The error")
    return engine 


def query_table():
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
    
    model_id = 'model_labse_ru_geonames'
    labse = SentenceTransformer(model_id)
    embeddings = labse.encode(names)
    embedding = pd.DataFrame({"embedding_values": [embedding.tolist() for embedding in embeddings]})
    data['embedding'] = embedding['embedding_values']
    
    data.to_sql('embeddings_lapse', con=engine.connect(), if_exists='replace')
    
    return names, embeddings, labse

def find_similar_labse(geoname, names, embeddings, model, top_k=3):
    response = pd.DataFrame(util.semantic_search(query_embeddings= model.encode(geoname), corpus_embeddings=embeddings, top_k=top_k)[0])
    return  response.assign(name=names[response.corpus_id])

def result_model(city):
     
    index_list = []    
    for i in res.values:
        index_list.append(i[0])  
    query_emb = "SELECT geonameid, name, region, country FROM embeddings_lapse WHERE index = ANY(:indexes)"
    res_emb = engine.connect().execute(text(query_emb).bindparams(indexes=index_list))
    
    response =  [item for item in res_emb]
    
    result = [] 
    for i, item in enumerate(response): 
      result.append({ 
        'geonameid': item[0], 
        'name': item[1], 
        'region': item[2], 
        'country': item[3], 
        'cosine_similarity': res.values[i][1] 
      }) 
    return result


if __name__ == "__main__":
    engine = create_connection("postgresql", "postgres", "1305", "localhost", "5432", "postgres")
    names, embeddings, labse = query_table()
    res = find_similar_labse(city, names, embeddings, labse)
    result = result_model(city)