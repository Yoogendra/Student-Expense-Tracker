from django.core.management.base import BaseCommand
from expenses.models import Category

class Command(BaseCommand):
    help = 'Create default expense categories'

    def handle(self, *args, **options):
        default_categories = [
            {'name': 'Food & Dining', 'description': 'Restaurants, groceries, and food delivery'},
            {'name': 'Transportation', 'description': 'Public transport, gas, parking, and ride-sharing'},
            {'name': 'Housing', 'description': 'Rent, utilities, and household supplies'},
            {'name': 'Education', 'description': 'Tuition, books, and school supplies'},
            {'name': 'Entertainment', 'description': 'Movies, games, and recreational activities'},
            {'name': 'Healthcare', 'description': 'Medical expenses, prescriptions, and insurance'},
            {'name': 'Shopping', 'description': 'Clothing, electronics, and personal items'},
            {'name': 'Subscriptions', 'description': 'Streaming services, software, and memberships'},
            {'name': 'Other', 'description': 'Miscellaneous expenses'},
        ]

        created_count = 0
        for category_data in default_categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new categories')
        )
