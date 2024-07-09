import folium
import json
from folium.features import DivIcon

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity, PokemonElementType
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, health, strength, defense, image_url=DEFAULT_IMAGE_URL):
    
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    data = f'Здоровье: {health}, Сила: {strength}, Защита: {defense}'
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        popup=data,
        icon=icon,
        ).add_to(folium_map)


def show_all_pokemons(request):
    current_time = localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=current_time,
        disappeared_at__gte=current_time
        ).select_related('pokemon')
    
    pokemons_on_page = []
    for entity in pokemon_entities:
        add_pokemon(
            folium_map, entity.lat,
            entity.lon,
            entity.health,
            entity.strength,
            entity.defense,
            entity.pokemon.photo.path,
            )

        pokemons_on_page.append({
            'pokemon_id': entity.pokemon.id,
            'img_url': entity.pokemon.photo.url,
            'title_ru': entity.pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)
    element_types = PokemonElementType.objects.filter(pokemon=pokemon)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_entity.health,
            pokemon_entity.strength,
            pokemon_entity.defense,
            pokemon.photo.path
        )
    
    pokemon_data = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'img_url': pokemon.photo.url,
        'description': pokemon.description
    }

    if pokemon.previous_evolution:
        pokemon_data['previous_evolution'] = {
            'title_ru': pokemon.previous_evolution.title,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': pokemon.previous_evolution.photo.url
        }

    next_evolution = pokemon.next_evolutions.first()
    if next_evolution:
        pokemon_data['next_evolution'] = {
            'title_ru': next_evolution.title,
            'pokemon_id': next_evolution.id,
            'img_url': next_evolution.photo.url
        }

    pokemon_data['element_type'] = []
    for element_type in element_types:
        pokemon_data['element_type'].append({
            'title': element_type.title,
            'img': element_type.img.url,
            'strong_against': list(element_type.strong_against.values_list('title', flat=True))
        })
                 
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 
        'pokemon': pokemon_data
    })