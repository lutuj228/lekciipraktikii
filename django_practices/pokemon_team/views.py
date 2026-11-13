
"""Представления для управления командой покемонов."""

import random

import requests

from django.shortcuts import render


POKEMON_API_URL = "https://pokeapi.co/api/v2/pokemon/"


def get_pokemon(name):
    """Получить характеристики покемона из PokéAPI.

    Args:
        name (str): Имя покемона для поиска.

    Returns:
        dict | None: Словарь с характеристиками покемона
        или None, если покемон не найден.
    """
    response = requests.get(
        f"{POKEMON_API_URL}{name}",
        timeout=10,
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()
    data = response.json()

    return {
        "name": data["name"],
        "image": data["sprites"]["front_default"],
        "height": data["height"],
        "weight": data["weight"],
        "types": [
            item["type"]["name"]
            for item in data["types"]
        ],
        "abilities": [
            item["ability"]["name"]
            for item in data["abilities"]
        ],
        "hp": data["stats"][0]["base_stat"],
        "attack": data["stats"][1]["base_stat"],
        "defense": data["stats"][2]["base_stat"],
    }


def team_view(request):
    """Обработать действия пользователя с командой покемонов.

    Поддерживает добавление и удаление покемонов, поиск
    по имени и тренировочный бой между двумя покемонами.
    Сохраняет состав команды в сессии Django.

    Args:
        request: HTTP-запрос пользователя.

    Returns:
        HttpResponse: HTML-страница с составом команды,
        результатами поиска и тренировочного боя.
    """
    team = request.session.get("pokemon_team", [])
    message = None
    search_result = None
    battle_result = None

    if request.method == "POST":
        action = request.POST.get("action")
        name = request.POST.get("name", "").strip().lower()

        if action == "add":
            if name in team:
                message = "Этот покемон уже есть в команде."
            elif name:
                pokemon = get_pokemon(name)

                if pokemon:
                    team.append(name)
                    request.session["pokemon_team"] = team
                    message = f"Покемон {name} добавлен в команду."
                else:
                    message = "Покемон не найден."

        elif action == "remove":
            if name in team:
                team.remove(name)
                request.session["pokemon_team"] = team
                message = f"Покемон {name} удалён из команды."

        elif action == "search":
            if name:
                search_result = get_pokemon(name)

                if not search_result:
                    message = "Покемон не найден."

        elif action == "battle":
            first = request.POST.get("first")
            second = request.POST.get("second")

            if first in team and second in team and first != second:
                pokemon_1 = get_pokemon(first)
                pokemon_2 = get_pokemon(second)

                if pokemon_1 and pokemon_2:
                    score_1 = (
                        pokemon_1["hp"]
                        + pokemon_1["attack"]
                        + random.randint(1, 20)
                    )
                    score_2 = (
                        pokemon_2["hp"]
                        + pokemon_2["attack"]
                        + random.randint(1, 20)
                    )

                    if score_1 > score_2:
                        winner = first
                    elif score_2 > score_1:
                        winner = second
                    else:
                        winner = "Ничья"

                    battle_result = {
                        "first": first,
                        "second": second,
                        "score_1": score_1,
                        "score_2": score_2,
                        "winner": winner,
                    }
                else:
                    message = "Не удалось получить данные покемонов."
            else:
                message = "Выберите двух разных покемонов из команды."

    pokemons = []

    for name in team:
        pokemon = get_pokemon(name)

        if pokemon:
            pokemons.append(pokemon)

    return render(
        request,
        "pokemon_team/team.html",
        {
            "pokemons": pokemons,
            "message": message,
            "search_result": search_result,
            "battle_result": battle_result,
        },
    )
