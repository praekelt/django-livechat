django-livechat
===============

django-livechat provides a simple application to enable a very rudimentary
"live" chat session around a selected topic. It is based on functionality
originally developed for the Ummeli website.

A LiveChat model can be instantiated on its own, or hanging of another content
type. It subclasses jmbo.ModelBase to use the commenting, moderating, likes,
etc. functionality provided by the jmbo framework.

In the admin site, on any live chat model's change form view, there is a new
button in the toolbar at the top right of the page to enable a moderator or
expert to participate in the livechat, and respond to questions or posts.

A context processor checks for active live chats, and will add it to the
request context for use in templates, and to modify URLs, if necessary.

There are template tags that will display an entire live chat and its comments
thread in a template, as well as to display a banner advertising an upcoming
live chat.


Dependencies
------------

### System libraries

- T.B.D.

### Python packages

- Django 1.4.5
- South 0.8.1
- jmbo 0.5.5                The version is important!

Other dependencies include:

- django-category 0.1.1
- django-likes 0.0.12
- django-photologue 2.7
- django-preferences 0.0.6
- django-publisher 0.0.3
- django-secretballot 0.2.3
- django-sites-groups 0.1.2
- django-tastypie 0.10.0
- python-dateutil 2.1

Usage
-----

For production, install the application with:

    python setup.py install

For development, install the application with:

    python setup.py develop

### Settings

The following settings must be added to settings.py:

    INSTALLED_APPS += (
        'livechat',
    )

The jmbo application and its dependecies should also be installed, but will probably
already be installed. Refer to the jmbo application's documentation for more
information.

You can add a context processor to add the newest live chat that is in progress
to the request context.


    TEMPLATE_CONTEXT_PROCESSORS += (
        "livechat.context_processors.current_livechat",
    )
