from setuptools import setup, find_packages

setup(
    name='django-livechat',
    version='1.0.0',
    description='Very Simple Live Chat Django Application',
    long_description = open('README.md', 'r').read() + \
            open('AUTHORS.md', 'r').read() + open('CHANGELOG.md', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/django-livechat',
    packages = find_packages(),
    dependency_links = [
    ],
    install_requires = [
        'django==1.4.5',
        'south==0.8.1',
        'jmbo==0.5.5',
        'pytest',
        'pytest-django',
        'pytest-cov',
        'pytest-xdist',
    ],
    tests_require=[
        'django-setuptest==0.1.4',
    ],
    test_suite="setuptest.setuptest.SetupTestSuite",
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
