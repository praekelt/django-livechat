DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'livechat_test.sqlite',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.comments',

    'livechat',
    'south',
    'jmbo',
    'secretballot',
    'category',
    'photologue',
    'publisher',
)

SITE_ID = 1

STATIC_URL = ''

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False
