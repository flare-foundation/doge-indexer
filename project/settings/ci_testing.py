from .common import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

TEST_RUNNER = "xmlrunner.extra.djangotestrunner.XMLTestRunner"

TEST_OUTPUT_FILE_NAME = "testreport.xml"

# For faster user tests
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

SEND_EMAIL_CONFIRMATIONS = False
