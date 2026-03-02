from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from menu.models import Category, Food, FoodImage, Topping, FoodTopping
from menu.utils.availability import is_food_available
from menu.utils.pricing import calculate_final_price
from django.utils.safestring import mark_safe

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_icon', 'foods_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'display_icon']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'icon', 'display_icon')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def display_icon(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />', obj.icon.url)
        return '-'
    display_icon.short_description = 'Icon'
    
    def foods_count(self, obj):
        return obj.foods.count()
    foods_count.short_description = 'Foods Count'

class FoodImageInline(admin.TabularInline):
    model = FoodImage
    extra = 1
    fields = ('image', 'display_image')
    readonly_fields = ('display_image',)
    
    def display_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" style="object-fit: cover; border-radius: 4px;" />')
        return mark_safe('-')
    display_image.short_description = 'Preview'

class FoodToppingInline(admin.TabularInline):
    model = FoodTopping
    extra = 1
    autocomplete_fields = ['topping']

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'display_header_image', 'price_display', 'discount_display', 'availability_status', 'created_at']
    list_filter = ['category', 'is_available', 'discount', 'created_at']
    search_fields = ['name', 'description', 'category__name']
    readonly_fields = ['created_at', 'updated_at', 'display_header_image', 'final_price_display']
    autocomplete_fields = ['category']
    inlines = [FoodImageInline, FoodToppingInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'description', 'header_image', 'display_header_image')
        }),
        ('Pricing', {
            'fields': ('price', 'discount', 'final_price_display')
        }),
        ('Availability', {
            'fields': ('is_available', 'available_from', 'available_to')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def display_header_image(self, obj):
        if obj.header_image:
            return mark_safe(f'<img src="{obj.header_image.url}" width="150" height="150" style="object-fit: cover; border-radius: 8px;" />')
        return '-'
    display_header_image.short_description = 'Header Image'
    
    def price_display(self, obj):
        return mark_safe(f'€{obj.price}')
    price_display.short_description = 'Price'
    
    def discount_display(self, obj):
        if obj.discount and obj.discount > 0:
            return mark_safe(f'<span style="color: #e74c3c; font-weight: bold;">{obj.discount}%</span>')
        return mark_safe('-')
    discount_display.short_description = 'Discount'
    
    def availability_status(self, obj):
        is_avail = is_food_available(obj)
        if is_avail:
            return mark_safe(f'<span style="color: #27ae60; font-weight: bold;">Available</span>')
        return mark_safe(f'<span style="color: #e74c3c; font-weight: bold;">Unavailable</span>')
    availability_status.short_description = 'Status'
    
    def final_price_display(self, obj):
        if obj.price is None:
            return mark_safe('-')
        final_price = calculate_final_price(obj.price, obj.discount)
        if obj.discount and obj.discount > 0:
            return mark_safe(
                '<span style="text-decoration: line-through; color: #95a5a6;">€{}</span> <span style="color: #e74c3c; font-weight: bold; font-size: 1.2em;">€{}</span>',
                obj.price, final_price
            )
        return mark_safe(f'<span style="font-weight: bold;">€{obj.price}</span>')
    final_price_display.short_description = 'Final Price'

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_display', 'discount_display', 'availability_status', 'created_at']
    list_filter = ['is_available', 'discount', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'final_price_display']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'discount', 'final_price_display')
        }),
        ('Availability', {
            'fields': ('is_available', 'available_from', 'available_to')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def price_display(self, obj):
        return mark_safe(f'€{obj.price}')
    price_display.short_description = 'Price'
    
    def discount_display(self, obj):
        if obj.discount and obj.discount > 0:
            return mark_safe(f'<span style="color: #e74c3c; font-weight: bold;">{obj.discount}%</span>')
        return mark_safe('-')
    discount_display.short_description = 'Discount'
    
    def availability_status(self, obj):
        now = timezone.now().time()
        if not obj.is_available:
            return mark_safe(f'<span style="color: #e74c3c; font-weight: bold;">Unavailable</span>')
        if obj.available_from and obj.available_to:
            if obj.available_from <= obj.available_to:
                is_avail = obj.available_from <= now <= obj.available_to
            else:
                is_avail = now >= obj.available_from or now <= obj.available_to
            if is_avail:
                return mark_safe(f'<span style="color: #27ae60; font-weight: bold;">Available</span>')
            return mark_safe(f'<span style="color: #e74c3c; font-weight: bold;">Unavailable</span>')
        return mark_safe(f'<span style="color: #27ae60; font-weight: bold;">Available</span>')
    availability_status.short_description = 'Status'
    
    def final_price_display(self, obj):
        if obj.price is None:
            return '-'
        final_price = calculate_final_price(obj.price, obj.discount)
        if obj.discount and obj.discount > 0:
            return mark_safe(
                '<span style="text-decoration: line-through; color: #95a5a6;">€{}</span> <span style="color: #e74c3c; font-weight: bold; font-size: 1.2em;">€{}</span>',
                obj.price, final_price
            )
        return mark_safe(f'<span style="font-weight: bold;">€{obj.price}</span>')
    final_price_display.short_description = 'Final Price'

@admin.register(FoodTopping)
class FoodToppingAdmin(admin.ModelAdmin):
    list_display = ['food', 'topping', 'created_at']
    list_filter = ['created_at', 'food__category']
    search_fields = ['food__name', 'topping__name']
    autocomplete_fields = ['food', 'topping']
    readonly_fields = ['created_at', 'updated_at']
