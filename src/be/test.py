import os
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd 
from sklearn.neighbors import NearestNeighbors
import flask
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SECRET_KEY")
supabase: Client = create_client(url, key)

def KNN(): 
  response = supabase.table("dataUser").select("*").execute()
  df = pd.DataFrame(response.data)
  df = df.drop(['id'],axis=1)
  unit= pd.read_csv('dataset_unit.csv')
  feature_cols = unit.drop(['Nama Unit'], axis=1)
  X = feature_cols
  neigh = NearestNeighbors(n_neighbors=2, algorithm='brute')
  neigh.fit(X)
  data_dummy = df.iloc[len(df)-1].values.reshape(1,-1)
  distances, indices = neigh.kneighbors(data_dummy)
  print('Recommendations for "The Post":\n')
  for i in range(len(distances.flatten())):
    print('{0}: {1}, with a distance of {2}.'.format(i+1, unit['Nama Unit'].iloc[indices.flatten()[i]],distances.flatten()[i]))
  return unit['Nama Unit'].iloc[indices.flatten()[0]], distances.flatten()[0]


api = flask.Flask(__name__)


@api.route('/profile', methods =['GET'])
def my_profile():
    if flask.request.method == 'GET': 
      namaUnit,score = KNN()
      response_body = {
          "name": namaUnit,
          "about" :score
      }

    return response_body
