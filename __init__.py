from _version import __version__

API_VERSION = '1.0'

from httplib2 import Http
import oauth2 as oauth
from urlparse import urljoin
import time

from jsonutil import jsonutil as json

# example: http://api.simplegeo.com/0.1/context/37.797476,-122.424082.json

class Client(object):
    realm = "http://api.simplegeo.com"
    endpoints = {
        'context': 'context/%(lat)s,%(lon)s.json',
    }

    def __init__(self, key, secret, api_version=API_VERSION, host="api.simplegeo.com", port=80):
        self.host = host
        self.port = port
        self.consumer = oauth.Consumer(key, secret)
        self.key = key
        self.secret = secret
        self.api_version = api_version
        self.signature = oauth.SignatureMethod_HMAC_SHA1()
        self.uri = "http://%s:%s" % (host, port)
        self.http = Http()

    def endpoint(self, name, **kwargs):
        try:
            endpoint = self.endpoints[name]
        except KeyError:
            raise Exception('No endpoint named "%s"' % name)
        try:
            endpoint = endpoint % kwargs
        except KeyError, e:
            raise TypeError('Missing required argument "%s"' % (e.args[0],))
        return urljoin(urljoin(self.uri, self.api_version + '/'), endpoint)

    def get_context(self, lat, lon):
        endpoint = self.endpoint('context', lat=lat, lon=lon)
        return self._request(endpoint, "GET")

    def _request(self, endpoint, method):
        body = None
        params = {}
        request = oauth.Request.from_consumer_and_token(self.consumer,
            http_method=method, http_url=endpoint, parameters=params)

        request.sign_request(self.signature, self.consumer, None)
        headers = request.to_header(self.realm)
        headers['User-Agent'] = 'SimpleGeo Places Client v%s' % __version__

        resp, content = self.http.request(endpoint, method, body=body, headers=headers)

        if resp['status'][0] not in ('2', '3'):
            raise APIError(int(resp['status']), content, resp)

        if content: # Empty body is allowed.
            try:
                content = json.loads(content)
            except (ValueError, TypeError), le:
                raise DecodeError(resp, content, le)

        return content

class APIError(Exception):
    """Base exception for all API errors."""

    def __init__(self, code, msg, headers, description=''):
        self.code = code
        self.msg = msg
        self.headers = headers
        self.description = description

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "%s (#%s) %s" % (self.msg, self.code, self.description)

class DecodeError(APIError):
    """There was a problem decoding the API's JSON response."""

    def __init__(self, headers, body, le):
        super(DecodeError, self).__init__(None, "Could not decode JSON", headers, repr(le))
        self.body = body

    def __repr__(self):
        return "<%s headers: %s, content: %s , description: %s>" % (self.__class__.__name__, self.headers, self.body, self.description)

