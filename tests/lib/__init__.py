# -*- coding: utf-8 -*-

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lib.site.settings')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
os.environ['RECAPTCHA_TESTING'] = 'True'
