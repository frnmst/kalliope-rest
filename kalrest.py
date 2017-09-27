#!/usr/bin/env python3

# kalrest.py
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

import requests
import magic
import argparse
import configparser
import os
import sys

CONFIGURATION_FILE = "kalrest.conf"

class Kr():

    def __init__(self):

        self.parser = self._create_parser()
        self.configuration = self._parse_configuration()
        self.base_uri = 'http://' + self.host + ":" + self.port

    def _parse_configuration(self):

        config = configparser.ConfigParser(os.environ, interpolation = configparser.BasicInterpolation())
        try:
            config.read(CONFIGURATION_FILE)

            # These variables are visible to the rest of the class.
            self.host = config.get('Network',
                                   'Host',
                                   fallback='127.0.0.1')
            self.port = config.get('Network',
                                   'Port',
                                   fallback='5000')
            self.username = config.get('Administration',
                                       'Username',
                                       fallback='admin')
            self.password = config.get('Administration',
                                       'Password',
                                       fallback='secret')
        except Exception as e:
            sys.stderr.write(str(e) + "\n")
            sys.stderr.write("Problem reading the configuration file. Unable to proceed.\n")
        finally:
            return config

    # kv
    #   kv
    #   sps
    #   sp <name>
    #   exec by-name <synapse-name>
    #   exec by-order <text-order>
    #   exec by-audio <audio-file>
    def _create_parser(self):

        parser = argparse.ArgumentParser(description='Kalliope REST API frontend')
        subparsers = parser.add_subparsers(dest='command')
        subparsers.required = True

        get_kalliope_version_prs = subparsers.add_parser('kv',help="Get the version of Kalliope")
        get_synapses_prs = subparsers.add_parser('sps',help="Get all the synapses")
        get_synapse_prs = subparsers.add_parser('sp',help="Get the selected synapse")
        execute_synapse_group = subparsers.add_parser('exec',help="Execute a synapse by different criterias")
        egp = execute_synapse_group.add_subparsers(dest='command')
        egp.required = True
        execute_by_name_prs = egp.add_parser('by-name')
        execute_by_order_prs = egp.add_parser('by-order')
        execute_by_audio_prs = egp.add_parser('by-audio')

        # Define the function callbacks.
        get_kalliope_version_prs.set_defaults(func=self.get_kalliope_version)
        get_synapses_prs.set_defaults(func=self.get_synapses)
        get_synapse_prs.set_defaults(func=self.get_synapse)
        execute_by_name_prs.set_defaults(func=self.execute_by_name)
        execute_by_order_prs.set_defaults(func=self.execute_by_order)
        execute_by_audio_prs.set_defaults(func=self.execute_by_audio)

        get_synapse_prs.add_argument('synapse_name',
                                     metavar="SYNAPSE_NAME",
                                     help="the synapse name")
        execute_by_name_prs.add_argument('synapse_name',
                                          metavar="SYNAPSE_NAME",
                                         help="the synapse name")
        execute_by_name_prs.add_argument('-v','--voice',
                                          help="output the audio",
                                          action="store_true")
        execute_by_order_prs.add_argument('order_string',
                                          metavar="ORDER_STRING",
                                          help="a textual version of the vocal order")
        execute_by_order_prs.add_argument('-v','--voice',
                                          help="output the audio",
                                          action="store_true")
        execute_by_audio_prs.add_argument('audio_file',
                                          metavar="FILE_NAME",
                                          help="an audio file containing the vocal order")
        execute_by_audio_prs.add_argument('-v','--voice',
                                          help="output the audio",
                                          action="store_true")

        return parser

    def _perform_voice_output(self,args):
        if args.voice:
            self.no_voice = 'false'
        else:
            self.no_voice = 'true'


    ################
    # The REST API #
    ################

    # GET /
    def get_kalliope_version(self, args):

        try:
            r = requests.get(self.base_uri + "/",auth=(self.username, self.password))
            data = r.json()
            print(data[u'Kalliope version'])
        except requests.exceptions.ConnectionError:
             sys.stderr.write("Unable to connect to server\n")

    # GET /synapses
    def get_synapses(self, args):

        try:
            r = requests.get(self.base_uri + "/synapses", auth=(self.username, self.password))
            print(r.text)
        except requests.exceptions.ConnectionError:
             sys.stderr.write("Unable to connect to server\n")

    # GET /synapses/<synapse_name>
    def get_synapse(self, args):

        try:
            r = requests.get(self.base_uri + "/synapses" + "/" + args.synapse_name, auth=(self.username, self.password))
            if r.status_code == 404:
                 sys.stderr.write("Synapse " + args.synapse_name + " not found\n")
            else:
                print(r.text)
        except requests.exceptions.ConnectionError:
             sys.stderr.write("Unable to connect to server\n")

    # POST /synapses/start/id/<synapse_name>
    def execute_by_name(self, args):

        try:
            self._perform_voice_output(args)
            payload = {'no_voice': self.no_voice}
            print(self.no_voice)
            r = requests.post(self.base_uri + "/synapses/start/id" + "/" + args.synapse_name,
                              json=payload,
                              auth=(self.username, self.password))
            if r.status_code == 404:
                sys.stderr.write("Unable to run " + args.synapse_name + ". Not found\n")
            elif r.status_code == 401:
                sys.stderr.write("Unauthorized to run synapse " + args.synapse_name + "\n")
            else:
                # Assume status_code being 200
                print(r.text)
        except requests.exceptions.ConnectionError:
             sys.stderr.write("Unable to connect to server\n")

    # POST /synapses/start/order
    def execute_by_order(self, args):

        try:
            self._perform_voice_output(args)
            payload = {'order': args.order_string, 'no_voice': self.no_voice}
            r = requests.post(self.base_uri + "/synapses/start/order",
                             json=payload,
                             auth=(self.username, self.password))
            if r.status_code == 404:
                sys.stderr.write("Unable to run " + args.order_string + ". Not found\n")
            elif r.status_code == 401:
                sys.stderr.write("Unauthorized to run synapse " + args.order_string + "\n")
            else:
                # Assume status_code being 200
                print(r.text)
        except requests.exceptions.ConnectionError:
             sys.stderr.write("Unable to connect to server\n")

    # POST /synapses/start/audio
    # Supported file types: WAV, MP3
    def execute_by_audio(self, args):

        try:
            mime_of_file = magic.from_file(args.audio_file, mime=True)
            if mime_of_file not in ['audio/wav', 'audio/x-wav', 'audio/mpeg3', 'audio/x-mpeg-3']:
                sys.stderr.write("File is not WAV or MP3\n")
            else:
                try:
                    self._perform_voice_output(args)
                    files = {'file': (args.audio_file, open(args.audio_file, 'rb'),
                             mime_of_file, {'Expires': '0'})}
                    payload = {'no_voice': self.no_voice}
                    r = requests.post(self.base_uri + "/synapses/start/audio",
                                      files=files,
                                      data=payload,
                                      auth=(self.username, self.password))
                    if r.status_code == 400:
                        sys.stderr.write("No file was sent to the server\n")
                    else:
                        # Assume status_code being 200
                        print(r.text)
                except Exception as e:
                    sys.stderr.write(str(e) + "\n")
        except FileNotFoundError:
            sys.stderr.write("File not found\n")

if __name__ == '__main__':

    kr = Kr()
    args = kr.parser.parse_args()
    args.func(args)
