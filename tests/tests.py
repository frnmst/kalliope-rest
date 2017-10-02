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
# The valid http texts have been taken from
# https://github.com/kalliope-project/kalliope/blob/master/Docs/rest_api.md

from unittest.mock import patch, mock_open, MagicMock
import unittest
import requests_mock
import json
import wave
import random
import struct
import magic
from kalliope_rest import Kr


class FakeArgs():

    def __init__(self):

        self.host = '127.0.0.1'
        self.port = '5000'
        self.username = 'admin'
        self.password = 'secret'
        self.synapse_name = ''
        self.voice = ''
        self.order_string = ''
        self.audio_file = ''

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
              text='a fake 200 text')
        self.assertEqual(self.kr.get_synapses(self.args),1)

        # Assert 401.
        m.get(uri,
              status_code = 401,
              text='a fake 401 text')
        self.assertEqual(self.kr.get_synapses(self.args),1)

        # Assert 404.
        m.get(uri,
              status_code = 404,
              text='a fake 404 text')
        self.assertEqual(self.kr.get_synapses(self.args),1)

        # Assert a generic HTTP error.
        m.get(uri,
              status_code = 500,
              text='a fake 500 text')
        self.assertEqual(self.kr.get_synapses(self.args),1)

    @requests_mock.mock()
    def test_get_synapse(self,m):

        uri = self.kr.base_uri + "/synapses"

        # Assert 200 with a valid synapse name.
        uri_1 = uri + "/" + "say-hello"
        self.args.synapse_name = 'say-hello'
        payload = {"synapses":{"name":"say-hello","neurons":[{"say":{"message":["Bonjourmonsieur"]}}],"signals":[{"order":"bonjour"}]}}
        json_payload = json.dumps(payload, sort_keys=True, indent=4)
        m.get(uri_1,
              status_code = 200,
              text=json_payload)
        self.assertEqual(self.kr.get_synapse(self.args),0)

        # Assert 200 with an invalid http text.
        m.get(uri_1,
              status_code = 200,
              text='a fake 200 text')
        self.assertEqual(self.kr.get_synapse(self.args),1)

        # Assert 401.
        m.get(uri_1,
              status_code = 401,
              text='a fake 401 text')
        self.assertEqual(self.kr.get_synapse(self.args),1)

        # Assert 404.
        m.get(uri_1,
              status_code = 404,
              text='a fake 404 text')
        self.assertEqual(self.kr.get_synapse(self.args),1)

        # Assert a generic HTTP error.
        m.get(uri_1,
              status_code = 500,
              text='a fake 500 text')
        self.assertEqual(self.kr.get_synapse(self.args),1)

    @requests_mock.mock()
    def test_execute_by_name(self,m):

        uri = self.kr.base_uri + "/synapses/start/id"

        # Assert 201 with a valid order
        uri_1 = uri + "/" + "say-hello"
        self.args.synapse_name = 'say-hello'
        self.args.voice = False
        # None is encoded as null in the json_payload.
        payload = {"matched_synapses":[{"matched_order":None,"neuron_module_list":[{"generated_message":"Bonjourmonsieur","neuron_name":"Say"}],"synapse_name":"say-hello-fr"}],"status":"complete","user_order":None}
        json_payload = json.dumps(payload, sort_keys=True, indent=4)
        m.post(uri_1,
              status_code = 201,
              text=json_payload)
        self.assertEqual(self.kr.execute_by_name(self.args),0)

        # Assert 201 with a valid order and voice enabled as parameter
        self.args.voice = True
        m.post(uri_1,
              status_code = 201,
              text=json_payload)
        self.assertEqual(self.kr.execute_by_name(self.args),0)

        # Assert 201 with an invalid http text.
        m.post(uri_1,
              status_code = 201,
              text='a fake 201 text')
        self.assertEqual(self.kr.execute_by_name(self.args),1)

        # Assert 401.
        m.post(uri_1,
              status_code = 401,
              text='a fake 401 text')
        self.assertEqual(self.kr.execute_by_name(self.args),1)

        # Assert 404.
        m.post(uri_1,
              status_code = 404,
              text='a fake 404 text')
        self.assertEqual(self.kr.execute_by_name(self.args),1)

        # Assert a generic HTTP error.
        m.post(uri_1,
              status_code = 500,
              text='a fake 500 text')
        self.assertEqual(self.kr.execute_by_name(self.args),1)

    @requests_mock.mock()
    def test_execute_by_order(self,m):

        uri = self.kr.base_uri + "/synapses/start/order"

        # Assert 201 with a valid order
        self.args.order_string = 'Bonjour'
        self.args.voice = False
        payload = {"matched_synapses":[{"matched_order":"Bonjour","neuron_module_list":[{"generated_message":"Bonjourmonsieur","neuron_name":"Say"}],"synapse_name":"say-hello-fr"}],"status":"complete","user_order":"bonjour"}
        json_payload = json.dumps(payload, sort_keys=True, indent=4)
        m.post(uri,
              status_code = 201,
              text=json_payload)
        self.assertEqual(self.kr.execute_by_order(self.args),0)

        # Assert 201 with a valid order and voice enabled as parameter
        self.args.voice = True
        m.post(uri,
              status_code = 201,
              text=json_payload)
        self.assertEqual(self.kr.execute_by_order(self.args),0)

        # Assert 201 with an invalid http text.
        m.post(uri,
              status_code = 201,
              text='a fake 201 text')
        self.assertEqual(self.kr.execute_by_order(self.args),1)

        # Assert 401.
        m.post(uri,
              status_code = 401,
              text='a fake 401 text')
        self.assertEqual(self.kr.execute_by_order(self.args),1)

        # Assert 404.
        m.post(uri,
              status_code = 404,
              text='a fake 404 text')
        self.assertEqual(self.kr.execute_by_order(self.args),1)

        # Assert a generic HTTP error.
        m.post(uri,
              status_code = 500,
              text='a fake 500 text')
        self.assertEqual(self.kr.execute_by_order(self.args),1)


    ## TODO: Add mocking for io operations here ##
    ## TODO: Fix "ResourceWarning: unclosed file"

    # From
    # https://soledadpenades.com/2009/10/29/fastest-way-to-generate-wav-files-in-python-using-the-wave-module/
    def _generate_fake_wav(self):

        noise_output = wave.open(self.args.audio_file, 'w')
        noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))

        for i in range(0, 100):
            value = random.randint(-32767, 32767)
            packed_value = struct.pack('h', value)
            noise_output.writeframes(packed_value)
            noise_output.writeframes(packed_value)

        noise_output.close()

    # I need to find a module like wave, but for mp3.
    def _generate_fake_mp3(self):

        pass

    def _generate_fake_non_mp3_wma(self):

        with open(self.args.audio_file, "w") as fake_file:
            fake_file.write("this is the content of a fake wav file\n")
        fake_file.close()

    @requests_mock.mock()
#    @patch('builtins.open', new_callable=mock_open)
    def test_execute_by_audio(self,req_mock): #,opn_mock):

        # This will be interesting: we need to create fake files which will
        # have headers for wav, mp3 or a generic file.
        # If it is either a fake mp3 or wav file, the execute_by_audio function
        # should return 0. However if it is a generic file the execute_by_audio
        # should return 1. We also need to trat the case of a non-existing
        # file.

        uri = self.kr.base_uri + "/synapses/start/audio"

        # Assert 201 with a valid wav file
        self.args.audio_file = 'noise.wav'
        self._generate_fake_wav()
        self.args.order_string = 'Bonjour'
        self.args.voice = False
        payload = {"matched_synapses":[{"matched_order":"Bonjour","neuron_module_list":[{"generated_message":"Bonjourmonsieur","neuron_name":"Say"}],"synapse_name":"say-hello-fr"}],"status":"complete","user_order":"bonjour"}
        json_payload = json.dumps(payload, sort_keys=True, indent=4)
        req_mock.post(uri,
              status_code = 201,
              text=json_payload)
        self.assertEqual(self.kr.execute_by_audio(self.args),0)

        # Assert 201 with a valid mp3 file
        self._generate_fake_mp3()
        pass

        # Assert failure because of incomatible file
        self.args.audio_file = 'no_noise.wav'
        self._generate_fake_non_mp3_wma()
        self.assertEqual(self.kr.execute_by_audio(self.args),1)


'''
class TestArgumentParser(unittest.TestCase):

    pass


class TestConfiguratorParser(unittest.TestCase):

    pass
'''

if __name__ == '__main__':

    unittest.main()
