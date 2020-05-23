from django.core.management.base import BaseCommand, CommandError
from market.models import Category, SubCategory, Product
from bs4 import BeautifulSoup
import requests
from django.core.files import File
import shutil
from backend.settings import BASE_DIR


STOP_WORDS = ["ООО", "ТОВ", "ТД", "ЧП", "ТМ", "Украин"]
URL = 'https://gastronoma.net'


def get_products(category, subcategory, url):
    print("Downloading products")
    result = requests.get(url, verify=False)
    soup = BeautifulSoup(result.text, 'html.parser')
    for item in soup.findAll('div', {'class': 'company_pic'}):
        img = item.find('img')
        in_stop = [i for i in STOP_WORDS if img.get('title').find(i) >= 0]
        if not in_stop and img.get('src').find('no_image') < 0:
            print(img.get('title'))
            pr = Product()
            pr.category = category
            pr.subcategory = subcategory
            pr.name = img.get('title')
            img_response = requests.get(URL+img.get('src'), stream=True, verify=False)
            # saving tmp file
            with open(BASE_DIR+'/tmp/tmp.png', 'wb') as out_file:
                shutil.copyfileobj(img_response.raw, out_file)
            with open(BASE_DIR+'/tmp/tmp.png', 'rb') as img_file:
                pr.image.save('cat.png', File(img_file), save=True)
            pr.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Clearing DB')
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Product.objects.all().delete()
        try:
            shutil.rmtree('{}/media'.format(BASE_DIR))
        except:
            pass

        # Loading and parsing the main page
        # URL = 'https://gastronoma.net'
        print('Start importing from {}'.format(URL))
        result = requests.get(URL, verify=False)
        soup = BeautifulSoup(result.text, 'html.parser')
        content = soup.find('div', {'class': 'body_20'})
        for img in content.findAll('img'):
            c = Category()
            c.name = img.get('alt')
            img_response = requests.get(URL+img.get('src'), stream=True, verify=False)
            # saving tmp file
            with open(BASE_DIR+'/tmp/tmp.png', 'wb') as out_file:
                shutil.copyfileobj(img_response.raw, out_file)
            with open(BASE_DIR+'/tmp/tmp.png', 'rb') as img_file:
                c.image.save('cat.png', File(img_file), save=True)
            c.save()
            print('Saving ... {}'.format(c.name))

            for subcat in img.find_parent('tr').find('div').findAll('a'):
                sc = SubCategory()
                sc.name = subcat.text
                sc.category = c
                sc.save()
                get_products(c, sc, subcat.get('href'))

                print('Saving sub-category... {}'.format(sc.name))

