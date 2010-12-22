API_VERSION = '1.0'

# example: http://api.simplegeo.com/0.1/context/37.797476,-122.424082.json

from simplegeo.shared import json_decode
from simplegeo.shared import Client as SGClient, is_valid_ip, is_valid_lat, is_valid_lon
from pyutil.assertutil import precondition

class Client(SGClient):
    def __init__(self, key, secret, api_version=API_VERSION, host="api.simplegeo.com", port=80):
        SGClient.__init__(self, key, secret, api_version=api_version, host=host, port=port)

        self.endpoints['context'] = 'context/%(lat)s,%(lon)s.json'
        self.endpoints['context_by_ip'] = 'context/%(ip)s.json'
        self.endpoints['context_by_my_ip'] = 'context/ip.json'

    def get_context(self, lat, lon):
        precondition(is_valid_lat(lat), lat)
        precondition(is_valid_lon(lon), lon)
        endpoint = self._endpoint('context', lat=lat, lon=lon)
        return json_decode(self._request(endpoint, "GET")[1])

    def get_context_by_ip(self, ipaddr):
        precondition(is_valid_ip(ipaddr), ipaddr)
        endpoint = self._endpoint('context_by_ip', ip=ipaddr)
        return json_decode(self._request(endpoint, "GET")[1])

    def get_context_by_my_ip(self):
        endpoint = self._endpoint('context_by_my_ip')
        return json_decode(self._request(endpoint, "GET")[1])

