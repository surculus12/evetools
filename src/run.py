import os
import django

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
    django.setup()
    
    from common import esi
    esi.create_type_db()
