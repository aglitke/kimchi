#
# Project Kimchi
#
# Copyright IBM, Corp. 2013
#
# Authors:
#  Adam Litke <agl@linux.vnet.ibm.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import template

import cherrypy
import re
import base64


SESSION_USER = 'userid'


def debug(msg):
    cherrypy.log.error(msg)


def check_auth_session():
    """
    A user is considered authenticated if we have an established session open
    for the user.
    """
    try:
        s = cherrypy.session[SESSION_USER]
        #cherrypy.session.regenerate()
        user = cherrypy.request.login = cherrypy.session[SESSION_USER]
        debug("Authenticated with session: %s, for user: %s" % (s, user))
    except KeyError:
        debug("Session not found")
        return False
    debug("Session found for user %s" % user)
    return True


def check_auth_httpba():
    """
    REST API users may authenticate with HTTP Basic Auth.  This is not allowed
    for the UI because web browsers would cache the credentials and make it
    impossible for the user to log out without closing their browser completely.
    """
    if not template.can_accept('application/json'):
        return False

    authheader = cherrypy.request.headers.get('AUTHORIZATION')
    if not authheader:
        debug("No authentication headers found")
        return False

    debug("Authheader: %s" % authheader)
    # TODO: what happens if you get an auth header that doesn't use basic auth?
    b64data = re.sub("Basic ", "", authheader)
    decodeddata = base64.b64decode(b64data.encode("ASCII"))
    # TODO: test how this handles ':' characters in username/passphrase.
    userid, password = decodeddata.decode().split(":", 1)

    return login(userid, password)


def login(userid, password):
    if not user_verify(userid, password):
        debug("User cannot be verified with the supplied password")
        return False
    debug("User verified, establishing session")
    cherrypy.session.regenerate()
    # This line of code is discussed in doc/sessions-and-auth.markdown
    cherrypy.session[SESSION_USER] = cherrypy.request.login = userid
    return True


def logout():
    userid = cherrypy.session.get(SESSION_USER, None)
    cherrypy.session[SESSION_USER] = cherrypy.request.login = None
    cherrypy.lib.sessions.expire()


def kimchiauth(*args, **kwargs):
    debug("Entering kimchiauth...")
    if check_auth_session():
        return

    if check_auth_httpba():
        return

    # Redirect the UI to the login page
    if template.can_accept_html():
        raise cherrypy.InternalRedirect('/login.html')

    if template.can_accept('application/json'):
        cherrypy.response.headers['WWW-Authenticate'] = 'Basic realm=kimchi'
    raise cherrypy.HTTPError("401 Unauthorized")

def user_verify(userid, password):
    """
    TODO: PAM integration
    """
    return True
