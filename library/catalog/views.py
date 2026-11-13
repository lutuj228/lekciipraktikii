
from django.http import Http404
from django.shortcuts import render


BOOKS = [
    {
        "id": 1,
        "title": "Мастер и Маргарита",
        "author": "Михаил Булгаков",
        "year": 1967,
        "description": (
            "Роман о любви, добре и зле. "
            "В произведении переплетаются события "
            "в Москве и древнем Ершалаиме."
        ),
        "price": 1200,
    },
    {
        "id": 2,
        "title": "Преступление и наказание",
        "author": "Фёдор Достоевский",
        "year": 1866,
        "description": (
            "Роман о Родионе Раскольникове, "
            "его нравственных переживаниях, "
            "совести и ответственности за свои поступки."
        ),
        "price": 950,
    },
    {
        "id": 3,
        "title": "Война и мир",
        "author": "Лев Толстой",
        "year": 1869,
        "description": (
            "Роман-эпопея о жизни российского общества "
            "во время наполеоновских войн. "
            "Рассказывает о судьбах нескольких семей."
        ),
        "price": 1500,
    },
]


def book_list(request):
    """Отобразить список всех книг."""
    return render(
        request,
        "catalog/book_list.html",
        {"books": BOOKS},
    )


def book_detail(request, book_id):
    """Отобразить подробную информацию о выбранной книге."""
    for book in BOOKS:
        if book["id"] == book_id:
            return render(
                request,
                "catalog/book_detail.html",
                {"book": book},
            )

    raise Http404("Книга не найдена")
