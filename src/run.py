import os
import django

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
    django.setup()
    
#    from common import esi
#    esi.create_type_db()
#    esi.create_types_from_csv()

    import mains
    mains.get_month_stats()
