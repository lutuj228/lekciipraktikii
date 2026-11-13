
"""Представления для работы с PokéAPI."""

import requests

from django.shortcuts import render


def pokemon_list(request):
    """Отобразить список покемонов и сведения о выбранном покемоне.

    Получает первые 20 покемонов через PokéAPI.
    Если пользователь указал имя, запрашивает характеристики
    соответствующего покемона.

    Args:
        request: HTTP-запрос пользователя.

    Returns:
        HttpResponse: HTML-страница со списком покемонов
        и результатом поиска.
    """
    url = "https://pokeapi.co/api/v2/pokemon?limit=20"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    pokemons = response.json()["results"]

    pokemon_info = None
    error = None

    pokemon_name = request.GET.get("name", "").strip().lower()

    if pokemon_name:
        pokemon_url = (
            f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        )

        pokemon_response = requests.get(
            pokemon_url,
            timeout=10,
        )

        if pokemon_response.status_code == 200:
            data = pokemon_response.json()

            pokemon_info = {
                "name": data["name"],
                "types": [
                    item["type"]["name"]
                    for item in data["types"]
                ],
                "weight": data["weight"],
                "height": data["height"],
                "abilities": [
                    item["ability"]["name"]
                    for item in data["abilities"]
                ],
            }
        else:
            error = "Покемон не найден."

    return render(
        request,
        "pokemon_api/pokemon_list.html",
        {
            "pokemons": pokemons,
            "pokemon_info": pokemon_info,
            "error": error,
        },
    )
