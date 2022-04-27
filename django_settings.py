import sys
import os

SETTINGS_FILE = "main.settings.local"
# SETTINGS_FILE = "main.settings.append_data_remote"

# add the current directory to path so that we can find our settings files:
sys.path.append(os.path.dirname(__file__))

# SECRET should be set when virtualenv as activated.  Just incase its not
os.environ["SECRET_KEY"] = "\xb1>\xf3\x10\xd3p\x07\x8fS\x94'\xe3g\xc6cZ4\xb0R"

# taken from manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_FILE)

if "DJANGO_SETTINGS_MODULE" in os.environ:
    # from django.db.models.loading import get_models
    import django
    from django.apps import apps
    from django.test.client import Client
    from django.test.utils import setup_test_environment, teardown_test_environment
    from django.conf import settings as S

    django.setup()

    class DjangoModels(object):
        def __init__(self):
            for m in apps.get_models():
                setattr(self, m.__name__, m)

    A = DjangoModels()
    C = Client()
