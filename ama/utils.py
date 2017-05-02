import os
import random
import string
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone
import markdown2


markdowner = markdown2.Markdown()
markdown = markdowner.convert


def get_random_name():
    random_name_file = 'endangered-animalia.txt'
    with open(os.path.join(settings.BASE_DIR, random_name_file), encoding='latin1') as fp:
        return random.choice(fp.readlines())


def get_random_slug():
    N = 8
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(N))


def get_expiry_delta():
    delta = 14
    # returns a wrapper because django model "default" is evaluated only once per instance
    # and thus require a function to return correct datetime when "default" is actually called
    return timezone.now() + timedelta(days=delta)
