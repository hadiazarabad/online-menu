from django.test import TestCase, Client
from django.urls import reverse
from menu.models import Category, Food


class MenuListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )
        self.food = Food.objects.create(
            category=self.category,
            name="Test Food",
            description="Test Description",
            price=10.00,
            is_available=True
        )
    
    def test_menu_list_view(self):
        response = self.client.get(reverse('menu_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Category")
        self.assertContains(response, "Test Food")
    
    def test_menu_list_view_with_unavailable_food(self):
        self.food.is_available = False
        self.food.save()
        response = self.client.get(reverse('menu_list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Food")
    
    def test_menu_list_empty(self):
        Food.objects.all().delete()
        Category.objects.all().delete()
        response = self.client.get(reverse('menu_list'))
        self.assertEqual(response.status_code, 200)

