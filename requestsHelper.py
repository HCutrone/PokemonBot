import requests
import json

POKEMONURL = "https://pokeapi.co/api/v2/pokemon/"
TYPEIDX = {"normal": 0, "fire": 1, "water": 2, "grass": 3, "electric": 4, "ice": 5, "fighting": 6, "poison": 7, "ground": 8, \
  "flying": 9, "psychic": 10, "bug": 11, "rock": 12, "ghost": 13, "dark": 14, "dragon": 15, "steel": 16, "fairy": 17}


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
    returnMsg += "**{}** - {}\n\n".format(name.title(), description)
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

  pkmnName = json_data["name"].title()
  
  types = [1] * 18
  pkmnTypes = []

  for type in json_data["types"]:
    # add the pokemon's type to the message
    pkmnTypes.append(type["type"]["name"].title())
    # get the current type's strenghts and weaknesses
    typeDefense(type["type"]["url"], types)
  typesStr = " and ".join(pkmnTypes)
  msg += f"{pkmnName} is {typesStr} type\n"
  
  resistant = []
  weak = []
  immune = []
  index = 0
  # interpret the types data after all types have been accounted for
  for num in types:
    type = list(TYPEIDX.keys())[list(TYPEIDX.values()).index(index)].title()
    if num > 1:
      # weak to
      # 2 = 2x
      # 3 = 4x
      # (num - 1) * 2
      power = str((num - 1) * 2)
      weak.append(f"{type}({power}x)")
    elif num < 0:
      # resistant to
      # -1 = .5x
      # -2 = .25x
      # num * (-1/2)
      power = str((-1/2) / float(num))
      resistant.append(f"{type}({power}x)")
    elif num == 0:
      # immune to
      immune.append(f"{type}")
    index += 1

  if len(weak) == 0:
    weakstr = "None"
  else:
    weakstr = ", ".join(weak)
  if len(resistant) == 0:
    resistantstr = "None"
  else:
    resistantstr = ", ".join(resistant)
  if len(immune) == 0:
    immunestr = "None"
  else:
    immunestr = ", ".join(immune)

  msg += f"Weak to:\t{weakstr}\nResistant to:\t{resistantstr}\nImmune to:\t{immunestr}"
  return msg

def typeOffense(url, types):
  # takes the url of a pokemon type and an array
  # the array represents the 18 pokemon types, with each index being each type
  # the array is initially filled with 0s
  # when the provided type is SUPER EFFECTIVE on another type, the val is ++
  type = requests.get(url)
  json_data = json.loads(type.text)
  # double damage to
  for relation in json_data["damage_relations"]:
    for type in relation["no_damage_to"]:
      currentType = TYPEIDX[type[0]["name"]]
      types[currentType] = 0

    for type in relation["half_damage_to"]:
      currentType = TYPEIDX[type[0]["name"]]
      if types[currentType] > 0:
        types[currentType] = -1
      elif types[currentType] < 0:
        types[currentType] -= 1

    for type in relation["double_damage_to"]:
      currentType = TYPEIDX[type[0]["name"]]
      types[currentType] += 1

  return

def typeDefense(url, types):
  # takes the url of a pokemon type and an array
  # the array represents the 18 pokemon types, with each index being each type
  # the array is initially filled with 0s
  # when the provided type is NOT VERY EFFECTIVE on another type, the val is ++
  type = requests.get(url)
  json_data = json.loads(type.text)

  for type in json_data["damage_relations"]["no_damage_from"]:
    currentType = TYPEIDX[type["name"]]
    types[currentType] = 0

  for type in json_data["damage_relations"]["half_damage_from"]:
    currentType = TYPEIDX[type["name"]]
    if types[currentType] == 1:
      types[currentType] = -1
    elif types[currentType] != 0:
      types[currentType] -= 1

  for type in json_data["damage_relations"]["double_damage_from"]:
    currentType = TYPEIDX[type["name"]]
    if types[currentType] == -1:
      types[currentType] = 1
    elif types[currentType] != 0:
      types[currentType] += 1

  return

def getEvolution(pokemon):
  # what if the pokemon does not evolve
  url = getEvolURL(pokemon)
  pkmn = requests.get(url)
  json_data = json.loads(pkmn.text)
  msg = ""
  current = json_data["chain"]["species"]["name"].title()
  for evolution in json_data["chain"]["evolves_to"]:
    next = evolution["species"]["name"].title()
    trigger = evolution["evolution_details"][0]["trigger"]["name"]
    # details = evolTrigger(evolution["evolution_details"])
    msg += f"{current} evolves to {next} by {trigger}.\n"

  return msg

def getEvolURL(pokemon):
  url = "https://pokeapi.co/api/v2/pokemon-species/" + pokemon
  pkmn = requests.get(url)
  json_data = json.loads(pkmn.text)
  return json_data["evolution_chain"]["url"]

def evolTrigger(details):
  return "Leveling up! FILL"

def getEntry(pokemon, ver):
  url = "https://pokeapi.co/api/v2/pokemon-species/" + pokemon
  pkmn = requests.get(url)
  json_data = json.loads(pkmn.text)
  msg = ""
  # pokemon species -> flavor_text_entries -> flavor_text
  for entry in json_data["flavor_text_entries"]:
    if (entry["language"]["name"] == "en") and (entry["version"]["name"] == ver):
      msg += entry["flavor_text"]
      break
  return msg
  