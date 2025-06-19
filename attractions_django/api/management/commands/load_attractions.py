from django.core.management.base import BaseCommand
from api.models import Attraction

SAMPLE_ATTRACTIONS = [
    {
        "name": "Красная площадь",
        "city": "Москва",
        "description": "Историческая площадь в центре Москвы.",
        "is_popular": True,
        "language": "ru",
        "tags": ["история", "архитектура", "центр"]
    },
    {
        "name": "Hermitage Museum",
        "city": "Санкт-Петербург",
        "description": "One of the largest and oldest museums in the world.",
        "is_popular": True,
        "language": "en",
        "tags": ["museum", "art", "history"]
    },
    {
        "name": "Остров Кижи",
        "city": "Карелия",
        "description": "Музей под открытым небом с деревянной архитектурой.",
        "is_popular": False,
        "language": "ru",
        "tags": ["деревянное_зодчество", "природа"]
    },
]

class Command(BaseCommand):
    help = "Загрузка тестовых достопримечательностей"

    def handle(self, *args, **options):
        created_count = 0
        for item in SAMPLE_ATTRACTIONS:
            obj, created = Attraction.objects.get_or_create(
                name=item["name"],
                city=item["city"],
                defaults={
                    "description": item["description"],
                    "is_popular": item["is_popular"],
                    "language": item["language"],
                    "tags": item["tags"],
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Добавлено: {obj.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Уже существует: {obj.name}"))

        self.stdout.write(self.style.SUCCESS(f"Итого добавлено: {created_count}"))
