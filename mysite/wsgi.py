"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv
import sys

if 'win' in sys.platform:
    project_folder = os.path.expanduser(r'~\Documents\blog_source\mysite')  # adjust as appropriate
else:
    project_folder = os.path.expanduser('~/blog_source/mysite')

load_dotenv(os.path.join(project_folder, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()
