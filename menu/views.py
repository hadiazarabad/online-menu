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
                foods.append({
                    'food': food,
                    'final_price': final_price,
                    'has_discount': food.discount and food.discount > 0,
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
