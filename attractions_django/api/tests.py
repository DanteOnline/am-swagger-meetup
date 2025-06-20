from mixer.backend.django import mixer
from rest_framework.test import APITestCase
from api.models import Attraction
from api.serializers import AttractionSerializer


class AttractionsAPITestCase(APITestCase):

    def setUp(self):
        self.attractions_count = 3
        self.attractions = mixer.cycle(self.attractions_count).blend(Attraction)
        self.one_attraction = self.attractions[self.attractions_count-1]
        self.attraction_data ={
            "name": "Красная площадь",
            "city": "Москва",
            "description": "Историческая площадь в центре Москвы.",
            "is_popular": True,
            "language": "ru",
            "tags": ["история", "архитектура", "центр"]
        }

    def test_post(self):
        """
        Test /api/attractions/ - post, create
        """
        url = '/api/attractions/'
        response = self.client.post(url, data=self.attraction_data, format='json')
        self.assertEqual(201, response.status_code)
        response_json = response.json()
        del response_json['id']
        self.assertEqual(self.attraction_data, response_json)

    def test_get_list(self):
        """
        Test: /api/attractions/ - get, read, list
        """
        url = '/api/attractions/'
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(self.attractions_count, len(response.json()))

    def test_get_detail(self):
        """
        Test: /api/attractions/<int:pk>/ - get, read, detail
        """
        attraction = self.one_attraction
        url = f'/api/attractions/{attraction.id}/'
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        serializer = AttractionSerializer(attraction)
        expected_data = serializer.data
        self.assertEqual(expected_data, response.json())

    def test_put(self):
        """
        Test /api/attractions/<int:pk>/ - put, update
        """
        attraction = self.one_attraction
        url = f'/api/attractions/{attraction.id}/'
        attraction_data = self.attraction_data
        response = self.client.put(url, data=attraction_data, format='json')
        self.assertEqual(200, response.status_code)
        attraction_data['id'] = self.one_attraction.id
        self.assertEqual(attraction_data, response.json())

    def test_patch(self):
        """
        Test /api/attractions/<int:pk>/ - patch, update
        """
        attraction = self.one_attraction
        url = f'/api/attractions/{attraction.id}/'
        name = 'Patching name'
        response = self.client.patch(url, data={'name': name}, format='json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(name, response.json()['name'])

    def test_delete(self):
        """
        Test /api/attractions/<int:pk>/ - delete, delete
        """
        attraction = self.one_attraction
        self.assertTrue(Attraction.objects.filter(id=attraction.id).exists())
        url = f'/api/attractions/{attraction.id}/'
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
        self.assertFalse(Attraction.objects.filter(id=attraction.id).exists())

    def test_options(self):
        """
        Test /api/attractions/, /api/attractions/<int:pk>/ - options
        :return:
        """
        url = '/api/attractions/'
        response = self.client.options(url)
        self.assertEqual(200, response.status_code)

        url = f'/api/attractions/{self.one_attraction.id}/'
        response = self.client.options(url)
        self.assertEqual(200, response.status_code)
