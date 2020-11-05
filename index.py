from flask import Flask
import requests
from requests.exceptions import HTTPError
from flask_sqlalchemy import SQLAlchemy

# activate venv
# source venv/bin/activate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/Pokemon'
db = SQLAlchemy(app)


def poke_to_dict(api_url):
    # try and access the pokemon api
    try:
        # get the content
        response = requests.get(api_url)
        response.raise_for_status()
        # access JSOn content
        jr = response.json()
        # create a dict that will get the pokemon from the kanto pokedex
        pokemon = {}
        # for each pokemon in the kanto pokedex
        for i in range(0,len(jr['pokemon_entries'])):
            # get the make a get request to access the specific pokemon's page
            r2 = requests.get(f"https://pokeapi.co/api/v2/pokemon/{jr['pokemon_entries'][i]['pokemon_species']['name']}")
            r2.raise_for_status()
            # r2 is the request that stores all of the attributes of that pokemon
            attr = r2.json()
            # save the attributes based on the id of the pokemon
            pokemon[i] = {'id': attr['id'], 'attributes': attr}
            print(pokemon[i]['id'])

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    return pokemon

@app.route('/', methods=['GET'])
def index():
    descrip_url = "https://pokeapi.co/api/v2/pokedex/kanto"
    r = requests.get(descrip_url)
    return r.json()

descrip_url = "https://pokeapi.co/api/v2/pokedex/kanto"
pokemon = poke_to_dict(descrip_url)
# pokemon_table = Table.from_dict(pokemon,
#                            'pokemon_table',
#                            metadata,
#                            primary_key = 'id')

class Pokemon(db.Model):
    __tablename__ = 'Alex'
    pokemon_id = db.Column(
        db.Integer,
        primary_key=True)

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)

    def __repr__(self):
        return '<pokemon_id {}>'.format(self.pokemon_id)

db.create_all()

p1 = Pokemon(pokemon[0])
db.session.add(p1)
db.session.commit()