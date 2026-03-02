from datetime import datetime
from django.shortcuts import render
from menu.models import Category
from menu.utils.availability import is_food_available
from menu.utils.pricing import calculate_final_price
from menu.constants.templates import MENU_TEMPLATE

base_context = {
    'current_year': datetime.now().strftime('%Y'),
}

def menu_list(request):
    categories = Category.objects.prefetch_related(
        'foods__images',
        'foods__food_toppings__topping',
    ).all()
    
    menu_data = []
    for category in categories:
        foods = []
        for food in category.foods.all():
            if is_food_available(food):
                final_price = calculate_final_price(food.price, food.discount)
                image_urls = []
                if food.header_image:
                    image_urls.append(request.build_absolute_uri(food.header_image.url))
                for fi in food.images.all():
                    if fi.image:
                        url = request.build_absolute_uri(fi.image.url)
                        if url not in image_urls:
                            image_urls.append(url)
                available_toppings = []
                for ft in food.food_toppings.select_related('topping').all():
                    t = ft.topping
                    if t.is_available:
                        tp_final = calculate_final_price(t.price, t.discount or 0)
                        available_toppings.append({
                            'topping': t,
                            'final_price': tp_final,
                            'has_discount': t.discount and t.discount > 0,
                        })
                foods.append({
                    'food': food,
                    'final_price': final_price,
                    'has_discount': food.discount and food.discount > 0,
                    'image_urls': image_urls,
                    'available_toppings': available_toppings,
                })
        
        if foods:
            menu_data.append({
                'category': category,
                'foods': foods,
            })
    
    context = {
        'menu_data': menu_data,
    }
    return render(request, MENU_TEMPLATE, {**base_context, **context})
