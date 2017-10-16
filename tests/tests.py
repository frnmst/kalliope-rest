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

import requests
import unittest
import requests_mock
import json
import wave
import random
import struct
import magic
import pyfakefs
from pyfakefs.fake_filesystem_unittest import Patcher
from sys import stdout, stderr
from kalliope_rest import api, cli


class TestRestApi(pyfakefs.fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()
        self.username = 'admin'
        self.password = 'secret'
        self.base_uri = 'http://127.0.0.1:5000'
        self.synapse_name = 'say-hello'
        self.voice = True
        self.order = 'Bonjour'
        self.audio_file = ''

    @requests_mock.mock()
    def _abstract_requests_get_test(self,uri,json_payload,api_function,m):

        # Assert 200 with a valid http text.
        m.get(uri,
              status_code = 200,
              text=json_payload)
        self.assertEqual(api_function(),json_payload)

        # Assert 200 with an invalid http text. Assert raises the json error.
        m.get(uri,
              status_code = 200,
              text='a fake 200 text')
        with self.assertRaises(json.decoder.JSONDecodeError):
            api_function()

        # Simulate a connection error and assert that the connection error is
        # raised.
        m.get(uri,
              exc=requests.exceptions.ConnectionError)
        with self.assertRaises(requests.exceptions.RequestException):
            api_function()

    @requests_mock.mock()
    def _abstract_requests_post_test(self,uri,json_payload,api_function,m):
        # Assert 201 with a valid order and voice disabled as parameter.
        m.post(uri,
              status_code = 201,
              text=json_payload)
        self.assertEqual(api_function(),json_payload)

        # Assert 201 with an invalid http text.
        m.post(uri,
              status_code = 201,
              text='a fake 201 text')
        with self.assertRaises(json.decoder.JSONDecodeError):
            api_function()

        # Simulate a connection error and assert that the connection error is
        # raised.
        m.post(uri,
              exc=requests.exceptions.ConnectionError)
        with self.assertRaises(requests.exceptions.RequestException):
            api_function()

    def test_get_kalliope_version(self):
        json_payload =  json.dumps({'Kalliope version':'0.4.5'}, sort_keys=True, indent=4)
        self._abstract_requests_get_test(
            self.base_uri + "/",
            json_payload,
            lambda: api.get_kalliope_version(base_uri=self.base_uri,
                                             username=self.username,
                                             password=self.password))

    def test_get_synapses(self):
        payload = {"synapses":[[{"name":"stop-kalliope","neurons":[{"say":{"message":"Goodbye"}},"kill_switch"],"signals":[{"order":"close"}]}],[{"name":"say-hello","neurons":[{"say":{"message":["Bonjourmonsieur"]}}],"signals":[{"order":"bonjour"}]}]]}
        json_payload = json.dumps(payload, sort_keys=True, indent=4)
        self._abstract_requests_get_test(
            self.base_uri + "/synapses",
            json_payload,
            lambda: api.get_synapses(base_uri=self.base_uri,
                                         username=self.username,
                                         password=self.password))

    def test_get_synapse(self):
        payload = {"synapses":{"name":"say-hello","neurons":[{"say":{"message":["Bonjourmonsieur"]}}],"signals":[{"order":"bonjour"}]}}
        json_payload = json.dumps(payload, sort_keys=True, indent=4)
        self._abstract_requests_get_test(
            self.base_uri + "/synapses" + "/" + self.synapse_name,
            json_payload,
            lambda: api.get_synapse(base_uri=self.base_uri,
                                        username=self.username,
                                        password=self.password,
                                        synapse_name=self.synapse_name))

    def test_get_listening_status(self):
        payload = {"mute":True}
        json_payload = json.dumps(payload, sort_keys=True, indent=4)
        self._abstract_requests_get_test(
            self.base_uri + "/mute",
            json_payload,
            lambda: api.get_listening_status(base_uri=self.base_uri,
                                             username=self.username,
                                             password=self.password))

    def test_execute_by_name(self):
        # None is encoded as null in the json_payload.
        payload = {"matched_synapses":[{"matched_order":None,"neuron_module_list":[{"generated_message":"Bonjourmonsieur","neuron_name":"Say"}],"synapse_name":"say-hello-fr"}],"status":"complete","user_order":None}
        json_payload = json.dumps(payload, sort_keys=True, indent=4)
        # As far as I can tell setting the voice option does not alter the
        # server's response. For this reason, we will keep the voice variable
        # enabled by default.
        self._abstract_requests_post_test(
            self.base_uri + "/synapses/start/id" + "/" + self.synapse_name,
            json_payload,
            lambda: api.execute_by_name(base_uri=self.base_uri,
                                            username=self.username,
                                            password=self.password,
                                            synapse_name=self.synapse_name,
                                            voice=self.voice))

    def test_execute_by_order(self):
        payload = {"matched_synapses":[{"matched_order":"Bonjour","neuron_module_list":[{"generated_message":"Bonjourmonsieur","neuron_name":"Say"}],"synapse_name":"say-hello-fr"}],"status":"complete","user_order":"bonjour"}
        json_payload = json.dumps(payload, sort_keys=True, indent=4)
        self._abstract_requests_post_test(
            self.base_uri + "/synapses/start/order",
            json_payload,
            lambda: api.execute_by_order(base_uri=self.base_uri,
                                            username=self.username,
                                            password=self.password,
                                            order=self.order,
                                            voice=self.voice))

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

    ## TODO I need to find a module like wave, but for mp3.
    def _generate_fake_mp3(self):
        pass

    def _generate_fake_non_mp3_wma(self):
        with open(self.args.audio_file, "w") as fake_file:
            fake_file.write("this is the content of a fake wav file\n")
        fake_file.close()

    @requests_mock.mock()
    def test_execute_by_audio(self,m):
        # This will be interesting: we need to create fake files which will
        # have headers for wav, mp3 or a generic file.
        # If it is either a fake mp3 or wav file, the execute_by_audio function
        # should return 0. However if it is a generic file the execute_by_audio
        # should return 1. We also need to trat the case of a non-existing
        # file.

        pass

        """
        uri = self.kr.base_uri + "/synapses/start/audio"

        self.fs.CreateFile('noise.wav')
        self.fs.CreateFile('no_noise.wav')

        # Assert 201 with a valid wav file
        self.args.audio_file = 'noise.wav'
        self._generate_fake_wav()
        self.args.order_string = 'Bonjour'
        self.args.voice = False
        payload = {"matched_synapses":[{"matched_order":"Bonjour","neuron_module_list":[{"generated_message":"Bonjourmonsieur","neuron_name":"Say"}],"synapse_name":"say-hello-fr"}],"status":"complete","user_order":"bonjour"}
        json_payload = json.dumps(payload, sort_keys=True, indent=4)
        m.post(uri,
              status_code = 201,
              text=json_payload)
        self.assertEqual(api.execute_by_audio(self.args),0)

        # Assert 201 with a valid mp3 file
        self._generate_fake_mp3()
        pass

        # Assert failure because of incomatible file
        self.args.audio_file = 'no_noise.wav'
        self._generate_fake_non_mp3_wma()
        self.assertEqual(api.execute_by_audio(self.args),1)
        """

class TestArgumentParser(unittest.TestCase):

    def setUp(self):

        self.kr = cli.CliInterface()
        self.kr.host = '127.0.0.1'
        self.kr.port = '5000'
        self.kr.username = 'admin'
        self.kr.password = 'secret'
        self.parser = self.kr.create_parser()

    # If the Sys exit exception is not handled, these unit tests would fail.
    def _handle_exit_code_exception(self,parameter_list):

        with self.assertRaises(SystemExit) as cm:
            parsed = self.parser.parse_args(parameter_list)
        return cm.exception.code

    def test_help(self):

        self.assertEqual(self._handle_exit_code_exception(['--help']), 0)
        self.assertEqual(self._handle_exit_code_exception(['-h']), 0)

    def test_version(self):

        self.assertEqual(self._handle_exit_code_exception(['--version']), 0)
        self.assertEqual(self._handle_exit_code_exception(['-v']), 0)

    def test_kv(self):

        self.assertEqual(
            str(
                self.parser.parse_args(['kv']).func.__name__),
            api.get_kalliope_version.__name__)

    def test_sps(self):

        self.assertEqual(
            str(
                self.parser.parse_args(['sps']).func.__name__),
           api.get_synapses.__name__)

    def test_sp(self):

        # Assert that it works with an argument
        self.assertEqual(
            str(
                self.parser.parse_args(['sp', 'fake_synapse_name']).func.__name__),
            api.get_synapse.__name__)

        # Assert that it fails without passing the synapse name.
        self.assertNotEqual(self._handle_exit_code_exception(['sp']), 0)

        # Assert that it fails with a non required argument.
        self.assertNotEqual(
            self._handle_exit_code_exception(['sp',
                                              'fake_synapse_name',
                                              'non required argument']),0)

    def test_listening(self):

        self.assertEqual(
            str(
                self.parser.parse_args(['listening']).func.__name__),
            api.get_listening_status.__name__)

    def test_exec(self):

        # Assert that it fails without passing the type of order.
        self.assertNotEqual(self._handle_exit_code_exception(['exec']), 0)

        # by-name
        self.assertEqual(
            str(
                self.parser.parse_args(['exec', 'by-name',
                                        'hello']).func.__name__),
            api.execute_by_name.__name__)
        self.assertNotEqual(self._handle_exit_code_exception(['exec', 'by-name']), 0)
        self.assertNotEqual(self._handle_exit_code_exception(['exec',
                                                              'by-name',
                                                              'hello',
                                                              'non required argument']), 0)

        # by-order
        self.assertEqual(
            str(
                self.parser.parse_args(['exec', 'by-order',
                                        'hello']).func.__name__),
            api.execute_by_order.__name__)
        self.assertNotEqual(self._handle_exit_code_exception(['exec', 'by-order']), 0)
        self.assertNotEqual(self._handle_exit_code_exception(['exec',
                                                              'by-order',
                                                              'hello',
                                                              'non required argument']), 0)

        # by-audio
        self.assertEqual(
            str(
                self.parser.parse_args(['exec', 'by-audio',
                                        'hello.wav']).func.__name__),
            api.execute_by_audio.__name__)
        self.assertNotEqual(self._handle_exit_code_exception(['exec', 'by-audio']), 0)
        self.assertNotEqual(self._handle_exit_code_exception(['exec',
                                                              'by-audio',
                                                              'hello.wav',
                                                              'non required argument']), 0)


"""
# TODO
class TestConfiguratorParser(pyfakefs.fake_filesystem_unittest.TestCase):

    def setUp(self):

        self.setUpPyfakefs()
        self.configuration = None

    def test__parse_configuration(self):

        pass
        #self.configuration = api(cli=True)._parse_configuration()
"""

if __name__ == '__main__':

    unittest.main()
