from django.shortcuts import render


def book_detail(request):
    book = {
        'title': 'Мастер и Маргарита',
        'author': 'Михаил Булгаков',
        'year': 1967,
        'description': 'Роман о любви, добре и зле.'
    }

    return render(request, 'catalog/book_detail.html', {
        'book': book
    })