
from django.shortcuts import render, redirect
from .models import Car
from .forms import CarForm
from django.db.models import Q, CharField
from django.db.models.functions import Cast

def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CarForm()
    return render(request, 'add_car.html', {'form': form})


def index(request):
    # Отримання параметрів сортування та пошуку
    sort_by = request.GET.get('sort', 'price')
    direction = request.GET.get('direction', 'asc')
    search_query = request.GET.get('search_query', '')

    # Фільтрація для текстових та рядкових полів
    text_query = Q(mark_name__icontains=search_query) | \
                 Q(model_name__icontains=search_query) | \
                 Q(generation_name__icontains=search_query) | \
                 Q(equipment_name__icontains=search_query) | \
                 Q(id__icontains=search_query)

    # Конвертування числових полів в рядки для фільтрації
    cars = Car.objects.annotate(
        str_year=Cast('year', CharField()),
        str_price=Cast('price', CharField())
    )
    numeric_query = Q(str_year__icontains=search_query) | Q(str_price__icontains=search_query)

    # Об'єднання текстових та числових запитів
    query = text_query | numeric_query
    if search_query.lower() == 'none':
        none_query = Q(mark_name__isnull=True) | \
                     Q(model_name__isnull=True) | \
                     Q(generation_name__isnull=True) | \
                     Q(equipment_name__isnull=True) | \
                     Q(year__isnull=True) | \
                     Q(price__isnull=True)
        query = query | none_query

    # Фільтрація та сортування
    if direction == 'desc':
        cars = cars.filter(query).order_by(f'-{sort_by}')
    else:
        cars = cars.filter(query).order_by(sort_by)

    # Передача даних до шаблону
    return render(request, 'index.html', {
        'cars': cars,
        'sort': sort_by,
        'direction': direction,
        'search_query': search_query
    })
