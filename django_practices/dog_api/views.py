
"""Представления для получения пород собак и их фотографий."""

import requests

from django.shortcuts import render


def dog_list(request):
    """Отобразить список пород и фотографии выбранных собак.

    Получает все породы и подпороды через Dog API.
    Обрабатывает названия пород, введённые через запятую,
    и запрашивает случайную фотографию для каждой из них.

    Args:
        request: HTTP-запрос пользователя.

    Returns:
        HttpResponse: HTML-страница со списком пород,
        фотографиями и сообщением об ошибке при её наличии.
    """
    url = "https://dog.ceo/api/breeds/list/all"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    breeds_data = response.json()["message"]

    breeds = []

    for breed, sub_breeds in breeds_data.items():
        if sub_breeds:
            for sub_breed in sub_breeds:
                breeds.append(f"{sub_breed} {breed}")
        else:
            breeds.append(breed)

    dog_images = {}
    error = None

    selected_breeds = request.GET.get("breeds", "")

    if selected_breeds:
        names = selected_breeds.lower().split(",")

        for name in names:
            name = name.strip()

            if not name:
                continue

            parts = name.split()

            if len(parts) == 2:
                breed_url = f"{parts[1]}/{parts[0]}"
            else:
                breed_url = name

            image_url = (
                f"https://dog.ceo/api/breed/{breed_url}/images/random"
            )

            image_response = requests.get(
                image_url,
                timeout=10,
            )

            if image_response.status_code == 200:
                dog_images[name] = image_response.json()["message"]
            else:
                error = "Некоторые породы не найдены."

    return render(
        request,
        "dog_api/dog_list.html",
        {
            "breeds": breeds,
            "dog_images": dog_images,
            "error": error,
        },
    )
