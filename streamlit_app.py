import streamlit as st
import pandas as pd
import numpy as np
import requests
import seaborn as sns
import matplotlib.pyplot as plt
from pprint import pprint


st.title("Pokemon Explorer")

pokemon_number = st.slider("Pick a pokemon!!",
                        1, 150, step=1)

url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_number}'
response = requests.get(url).json()
pokemon_name = response['name']
pokemon_height = response['height']
pokemon_weight = response['weight']
pokemon_cry = response['cries']['latest']
hp_stat = response['stats'][0]['base_stat']
attack_stat = response['stats'][1]['base_stat']
defense_stat = response['stats'][2]['base_stat']
special_attack_stat = response['stats'][3]['base_stat']
special_defense_stat = response['stats'][4]['base_stat']
speed_stat = response['stats'][5]['base_stat']

st.title(pokemon_name.title())
st.image(f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_number}.png", caption="")

if st.button("Click me to hear what I sound like!"):
    st.audio(pokemon_cry)

attributes = ['HP', 'Attack', 'Defense', 'Special Attack', 'Special Defense', 'Speed']

df = pd.DataFrame({
            'Attribute': attributes,
            'Stat': [hp_stat,attack_stat,defense_stat,special_attack_stat,special_defense_stat,speed_stat]
        })

st.write("### Pokémon Base Stats")
st.dataframe(df)

##Getting data of all pokemon first gen
pokedex = pd.DataFrame(columns = ['name', 'height', 'weight'])

def get_details(poke_number):
    try:
        url = f'https://pokeapi.co/api/v2/pokemon/{poke_number}/'
        response = requests.get(url)
        pokemon = response.json()
        return pokemon.get('name'), pokemon.get('height'), pokemon.get('weight') 
    except:
        return 'Error', np.NAN, np.NAN, np.NAN

    
for poke_number in range(1, 152):
    pokedex.loc[poke_number] = get_details(poke_number)

#Creating the graph
max_height = pokedex['height'].max()
min_height = pokedex['height'].min()
tallest_pokemon = pokedex.loc[pokedex['height'].idxmax()]['name']
shortest_pokemon = pokedex.loc[pokedex['height'].idxmin()]['name']

comparison_data = {
        'Pokemon': [shortest_pokemon, response['name'], tallest_pokemon],
        'Height': [min_height, response['height'], max_height]
    }

plt.figure(figsize=(6,4))
sns.barplot(x='Pokemon', y='Height', data=comparison_data)
plt.title('Heights in comparison to the tallest and shortest')
plt.xlabel('Pokemon')
plt.ylabel('Height (m)')
plt.savefig('heights.png')
plt.close()
st.image("heights.png")


max_weight = pokedex['weight'].max()
min_weight = pokedex['weight'].min()
smallest_pokemon = pokedex.loc[pokedex['weight'].idxmin()]['name']
biggest_pokemon = pokedex.loc[pokedex['weight'].idxmax()]['name']

comparison_data2 = {
        'Pokemon': [smallest_pokemon, response['name'], biggest_pokemon],
        'Weight': [min_weight, response['weight'], max_weight]
    }

plt.figure(figsize=(6,4))
sns.barplot(x='Pokemon', y='Weight', data=comparison_data2)
plt.title('Weights in comparison to the biggest and smallest')
plt.xlabel('Pokemon')
plt.ylabel('Weight (kg)')
plt.savefig('weights.png')
plt.close()

st.image("weights.png")