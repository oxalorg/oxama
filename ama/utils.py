import os
import random
import string

from django.conf import settings
import markdown2


markdowner = markdown2.Markdown()
markdown = markdowner.convert


random_name_file = 'endangered-animalia.txt'
def get_random_name():
    with open(os.path.join(settings.BASE_DIR, random_name_file), encoding='latin1') as fp:
        return random.choice(fp.readlines())


def get_random_slug():
    N = 8
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(N))
