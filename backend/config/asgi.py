"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import dotenv
from pathlib import Path
from django.core.asgi import get_asgi_application

dotenv.read_dotenv(Path(__file__).parent.parent / '.env')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
