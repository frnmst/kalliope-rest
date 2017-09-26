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
import argparse
import configparser
import os
import sys

CONFIGURATION_FILE = "kr.conf"

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
        execute_by_name_prs.add_argument('execute_by_name',
                                    metavar="SYNAPSE_NAME",
                                    help="the synapse name")
        execute_by_order_prs.add_argument('execute_by_order',
                                    metavar="ORDER_STRING",
                                    help="a textual version of the vocal order")
        execute_by_audio_prs.add_argument('execute_by_audio',
                                    metavar="FILE_NAME",
                                    help="an audio file containing the vocal order")

        return parser

    def get_kalliope_version(self, args):

        try:
            r = requests.get(self.base_uri + "/",auth=(self.username, self.password))
            data = r.json()
            print(data[u'Kalliope version'])
        except requests.exceptions.ConnectionError:
             sys.stderr.write("Unable to connect to server\n")

    def get_synapses(self, args):

        try:
            r = requests.get(self.base_uri + "/synapses", auth=(self.username, self.password))
            print(r.text)
        except requests.exceptions.ConnectionError:
             sys.stderr.write("Unable to connect to server\n")

    def get_synapse(self, args):

        try:
            r = requests.get(self.base_uri + "/synapses" + "/" + args.synapse_name, auth=(self.username, self.password))
            if r.status_code == 404:
                 sys.stderr.write("Synapse " + args.synapse_name + " not found\n")
            else:
                print(r.text)
        except requests.exceptions.ConnectionError:
             sys.stderr.write("Unable to connect to server\n")

    def execute_by_name(self, args):

        print("By name: " + str(args.execute_by_name))

    def execute_by_order(self, args):

        print("By order: " + str(args.execute_by_order))

    def execute_by_audio(self, args):

        print("By audio: " + str(args.execute_by_audio))

if __name__ == '__main__':

    kr = Kr()
    args = kr.parser.parse_args()
    args.func(args)
