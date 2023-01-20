from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product
from products.models import ProductCategory

class IndexViewTestCase(TestCase):
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path) #get-запрос к странице

        self.assertEqual(response.status_code, HTTPStatus.OK) # HTTPSTATUS.OK == 200
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')

class ProductsListViewTestCase(TestCase):
    fixtures = ['products.json', 'product_categories']

    def setUp(self):
        self.products = Product.objects.all()
    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        # self.assertEqual(response.status_code, HTTPStatus.OK)
        # self.assertEqual(response.context_data['title'], 'Store - Каталог')
        # self.assertTemplateUsed(response, 'products/products.html')
        self._common_tests(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))
        """
        query-set'ы нельзя сравнивать между собой. Даже если объекты внутри одинаковы, сами query-set'ы будут отличаться,
        т.к. созданы в разное время. Чтобы обойти ошибку можно завернуть query-set'ы в списки. 
        """

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': 1})
        response = self.client.get(path)

        # self.assertEqual(response.status_code, HTTPStatus.OK)
        # self.assertEqual(response.context_data['title'], 'Store - Каталог')
        # self.assertTemplateUsed(response, 'products/products.html')
        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id)[:3])
        )

    def _common_tests(self, response):
        """
        Внутренняя функция для класса - чтоыб не писать повторяющиеся тесты в предыдущих двух методах (см. выше
        закомментированные строки.). Название начинается с '_' - так обозначаются методы, используемые только внутри класса)
        """
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')

