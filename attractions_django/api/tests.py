from mixer.backend.django import mixer
from rest_framework.test import APITestCase
from api.models import Attraction


class AttractionsAPITestCase(APITestCase):

    def setUp(self):
        self.attractions_count = 3
        self.attractions = mixer.cycle(self.attractions_count).blend(Attraction)

    def test_post(self):
        """
        Test /api/attractions/ - post, create
        """
        url = '/api/attractions/'
        data = {
            "name": "Красная площадь",
            "city": "Москва",
            "description": "Историческая площадь в центре Москвы.",
            "is_popular": True,
            "language": "ru",
            "tags": ["история", "архитектура", "центр"]
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(201, response.status_code)
        response_json = response.json()
        del response_json['id']
        self.assertEqual(data, response_json)

    def test_get_list(self):
        """
        Test: /api/attractions/ - get, read, list
        """
        url = '/api/attractions/'
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(self.attractions_count, len(response.json()))

    # def test_get_detail(self):
    #     """
    #
    #     :return:
    #     """


