#!/usr/bin/env python3

# tests.py
#
# Copyright (c) 2017, Franco Masotti
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# See http://tech.jonathangardner.net/wiki/Python/Setuptools/Testing

#from unittest.mock import patch, mock_open, MagicMock
import unittest
import requests_mock
import json
from kalliope_rest import Kr

class FakeArgs():

    def __init__(self):

        self.host = '127.0.0.1'
        self.port = '5000'
        self.username = 'admin'
        self.password = 'secret'


class TestRestApi(unittest.TestCase):

    def setUp(self):

        self.kr = Kr()
        self.args = FakeArgs()

    @requests_mock.mock()
    def test_get_kalliope_version(self,m):

        uri = self.kr.base_uri + "/"

        # Assert 200 with a valid http text.
        json_payload =  json.dumps({'Kalliope version':'0.4.5'}, sort_keys=True, indent=4)
        m.get(uri,
              status_code = 200,
              text=json_payload)
        self.assertEqual(self.kr.get_kalliope_version(self.args),0)

        # Assert 200 with an invalid http text.
        m.get(uri,
              status_code = 200,
              text='a fake 200 text')
        self.assertEqual(self.kr.get_kalliope_version(self.args),1)

        # Assert 401.
        m.get(uri,
              status_code = 401,
              text='a fake 401 text')
        self.assertEqual(self.kr.get_kalliope_version(self.args),1)

        # Assert a generic HTTP error.
        m.get(uri,
              status_code = 500,
              text='a fake 500 text')
        self.assertEqual(self.kr.get_kalliope_version(self.args),1)


    @requests_mock.mock()
    def test_get_synapses(self,m):

        uri = self.kr.base_uri + "/synapses"

        # Assert 200 with a valid http text.
        payload = {"synapses":[[{"name":"stop-kalliope","neurons":[{"say":{"message":"Goodbye"}},"kill_switch"],"signals":[{"order":"close"}]}],[{"name":"say-hello","neurons":[{"say":{"message":["Bonjourmonsieur"]}}],"signals":[{"order":"bonjour"}]}]]}
        json_payload = json.dumps(payload, sort_keys=True, indent=4)
        m.get(uri,
              status_code = 200,
              text=json_payload)
        self.assertEqual(self.kr.get_synapses(self.args),0)

        # Assert 200 with an invalid http text.
        m.get(uri,
              status_code = 200,
              text='')
        self.assertEqual(self.kr.get_synapses(self.args),1)

        # Assert 401.
        m.get(uri,
              status_code = 401,
              text='')
        self.assertEqual(self.kr.get_synapses(self.args),1)

        # Assert 404.
        m.get(uri,
              status_code = 404,
              text='')
        self.assertEqual(self.kr.get_synapses(self.args),1)

        # Assert a generic HTTP error.
        m.get(uri,
              status_code = 500,
              text='')
        self.assertEqual(self.kr.get_synapses(self.args),1)

    '''
    def test_execute_by_name(self):

        pass

    def test_execute_by_order(self):

        pass

    def test_execute_by_audio(self):

        pass

    def test_get_kalliope_version(self):

        pass


    class TestArgumentParser(unittest.TestCase):

        pass

    class TestConfiguratorParser(unittest.TestCase):

        pass

    '''

if __name__ == '__main__':

    unittest.main()
