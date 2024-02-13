from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer

class ItemTests(APITestCase):
    def setUp(self):
        self.item1 = Item.objects.create(
            sku='SKU001',
            name='Test Item 1',
            category='Test Category',
            tags=['tag1', 'tag2'],
            stock_status='In Stock',
            available_stock=100
        )
        self.item2 = Item.objects.create(
            sku='SKU002',
            name='Test Item 2',
            category='Test Category',
            tags=['tag3', 'tag4'],
            stock_status='Out of Stock',
            available_stock=0
        )

    def test_get_items(self):
        url = reverse('item-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming 2 items are created in setUp()

    def test_create_item(self):
        url = reverse('item-list')
        data = {
            'sku': 'SKU003',
            'name': 'Test Item 3',
            'category': 'Test Category',
            'tags': ['tag5', 'tag6'],
            'stock_status': 'In Stock',
            'available_stock': 50
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 3)  # Assuming one item is created

    def test_item_serializer(self):
        serializer_data = ItemSerializer(instance=self.item1).data
        expected_data = {
            'sku': 'SKU001',
            'name': 'Test Item 1',
            'category': 'Test Category',
            'tags': ['tag1', 'tag2'],
            'stock_status': 'In Stock',
            'available_stock': 100
        }
        self.assertEqual(serializer_data, expected_data)
