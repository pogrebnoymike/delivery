from django.core.management.base import BaseCommand, CommandError
from backend.settings import DATA_DIR
from openpyxl import load_workbook
from market.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Clearing DB')
        Category.objects.all().delete()
        Product.objects.all().delete()

        print('Importing data')
        wb = load_workbook(DATA_DIR+'/price.xlsx')
        worksheet = wb.get_sheet_by_name(wb.get_sheet_names()[0]) # Get first Worksheet
        current_category = None

        for row in worksheet.rows:
            cat_id = row[1].value
            item = row[2].value

            if cat_id is None:
                print('Create a new category: {}'.format(item))
                current_category = Category()
                current_category.name = item
                current_category.save()

            else:
                print("Create a new product: {}".format(item))
                p = Product()
                p.name = item
                if current_category:
                    p.category = current_category
                p.save()
