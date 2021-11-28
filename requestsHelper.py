import requests
import json

POKEMONURL = "https://pokeapi.co/api/v2/pokemon/"

def get_popular():
  response = requests.get("https://api.themoviedb.org/3/movie/popular?api_key=c39d4ad3c8c63b8dfda3ebe17d456510")

  json_data = json.loads(response.text)

  msg = ""

  for movie in json_data["results"]:
    msg += "{}\n".format(movie["title"])
  return msg

def get_rated():
  response = requests.get("https://api.themoviedb.org/3/movie/top_rated?api_key=c39d4ad3c8c63b8dfda3ebe17d456510")

  json_data = json.loads(response.text)

  msg = ""

  for movie in json_data["results"]:
    msg += "{}\n".format(movie["title"])
  return msg

def inspire():
  inspiration = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(inspiration.text)
  quote = json_data[0]['q']
  author = json_data[0]['a']
  return quote + "\n- " + author

def pkmnJSON(pokemon):
  url = POKEMONURL + pokemon
  pokemon = requests.get(url)
  return json.loads(pokemon.text)

def getAbilities(pokemon):
  json_data = pkmnJSON(pokemon)
  returnMsg = ""
  idx = 1
  for ability in json_data["abilities"]:
    name = ability["ability"]["name"]
    description = getAbilityDes(ability["ability"]["url"])
    returnMsg += "**{}** - {}\n\n".format(name, description)
    idx += 1
  return returnMsg

def getAbilityDes(abilityURL):
  info = requests.get(abilityURL)
  json_data = json.loads(info.text)

  for entry in json_data["effect_entries"]:
    if entry["language"]["name"] == "en":
      return entry["short_effect"]

def getTypes(pokemon):
  json_data = pkmnJSON(pokemon)
  msg = ""
  for type in json_data["types"]:
    msg += "{} \n".format(type["type"]["name"])
  return msg

def getStrengths(pokemon):
  json_data = pkmnJSON(pokemon)
  msg = ""
  # double damage to
  return msg

def getWeaknesses(pokemon):
  json_data = pkmnJSON(pokemon)
  msg = ""
  # double damage from
  # half damage to?
  # no damage to?
  return msg