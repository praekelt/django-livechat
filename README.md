django-livechat
===============

django-livechat provides a simple application to enable a very rudimentary
"live" chat session around a selected topic.

There is functionality for administrators to create the initial chat theme,
and an expert to reply to chats during the live chat.


Dependencies
------------

### System libraries

- T.B.D.

### Python packages

- T.B.D.


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
