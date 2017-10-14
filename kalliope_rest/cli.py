# cli.py
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

import argparse
import configparser
import os
import sys
import appdirs
import pkg_resources
import ipaddress
from shutil import copyfile
from .api_exceptions import (AudioFileError,
                             AudioFileFormatError)
from .cli_exceptions import ConfigurationParsingError
from .api import (get_kalliope_version,
                  get_synapses,
                  get_synapse,
                  get_listening_status,
                  execute_by_name,
                  execute_by_order,
                  execute_by_audio)

class CliToApi():
    """ An interface to transform the argparse arguments to api variables and
        to call the api functions.
    """
    # Note: these are not recursive functions.

    def get_kalliope_version(self,args):
        return get_kalliope_version(args.base_uri,args.username,args.password)

    def get_synapses(self,args):
        return get_synapses(args.base_uri, args.username, args.password)

    def get_synapse(self,args):
        return get_synapse(args.base_uri, args.username, args.password, args.synapse_name)

    def get_listening_status(self,args):
        return get_listening_status(args.base_uri, args.username, args.password)

    def execute_by_name(self,args):
        return execute_by_name(args.base_uri, args.username, args.password, args.synapse_name, args.voice)

    def execute_by_order(self,args):
        return execute_by_order(args.base_uri, args.username, args.password, args.order, args.voice)

    def execute_by_audio(self,args):
        return execute_by_order(args.base_uri, args.username, args.password, args.audio_file, args.voice)

class CliInterface():

    def __init__(self):
        self.host = ''
        self.port = ''
        self.username = ''
        self.password = ''
        try:
            self.configuration = self.parse_configuration()
            self.parser = self.create_parser()
        except ConfigurationParsingError:
            raise

    def _create_user_config(self,cfg_file):
        # Create the user's configuration file.
        source = pkg_resources.resource_filename(__name__, 'kalliope_rest.conf.dist')
        shutils.copyfile(source,cfg_file)

    def parse_configuration(self):
        PORT_MIN = 1
        PORT_MAX = 65535
        config = configparser.ConfigParser(os.environ, interpolation = configparser.BasicInterpolation())
        try:
            # Inspired by https://stackoverflow.com/questions/40193112/python-setuptools-distribute-configuration-files-to-os-specific-directories
            cfg_dir = appdirs.user_config_dir('kalliope_rest')
            cfg_file = os.path.join(cfg_dir, 'kalliope_rest.conf')
            if not os.path.exists(cfg_dir):
                os.makedirs(cfg_dir)
            if not os.path.isfile(cfg_file):
                self._create_user_config(cfg_file)
            # End of inspired by.
            config.read(cfg_file)
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
            # Check if the host variable is a valid IPv4 or IPv6 address.
            ipaddress.ip_address(self.host)
            # Check that the port variable is contained in the correct range.
            if int(self.port) < PORT_MIN or int(self.port) > PORT_MAX:
                raise ValueError('Port number out of range')
        except (configparser.Error, ValueError) as e:
            raise ConfigurationParsingError

        return config

    def create_parser(self):
        parser = argparse.ArgumentParser(description='Kalliope REST API frontend',
                                         epilog = "Return values: 0 OK, 1 API Error, 2 Invalid command")
        subparsers = parser.add_subparsers(dest='command')
        subparsers.required = True

        get_kalliope_version_prs = subparsers.add_parser('kv',help="show the version of Kalliope")
        get_synapses_prs = subparsers.add_parser('sps',help="show information about all the available synapses")
        get_synapse_prs = subparsers.add_parser('sp',help="show information about the selected synapse")
        get_listening_status_prs = subparsers.add_parser('listening',help="tells if Kalliope is waiting for orders")
        execute_synapse_group = subparsers.add_parser('exec',help="execute a synapse by different criterias")
        egp = execute_synapse_group.add_subparsers(dest='command')
        egp.required = True
        execute_by_name_prs = egp.add_parser('by-name')
        execute_by_order_prs = egp.add_parser('by-order')
        execute_by_audio_prs = egp.add_parser('by-audio')

        self.base_uri = 'http://' + self.host + ":" + self.port

        # Define the function callbacks and parameters.
        get_kalliope_version_prs.set_defaults(
            func=CliToApi().get_kalliope_version,
            base_uri=self.base_uri,
            username=self.username,
            password=self.password)
        get_synapses_prs.set_defaults(
            func=CliToApi().get_synapses,
            base_uri=self.base_uri,
            username=self.username,
            password=self.password)
        get_synapse_prs.set_defaults(
            func=CliToApi().get_synapse,
            base_uri=self.base_uri,
            username=self.username,
            password=self.password)
        get_listening_status_prs.set_defaults(
            func=CliToApi().get_listening_status,
            base_uri=self.base_uri,
            username=self.username,
            password=self.password)
        execute_by_name_prs.set_defaults(
            func=CliToApi().execute_by_name,
            base_uri=self.base_uri,
            username=self.username,
            password=self.password)
        execute_by_order_prs.set_defaults(
            func=CliToApi().execute_by_order,
            base_uri=self.base_uri,
            username=self.username,
            password=self.password)
        execute_by_audio_prs.set_defaults(
            func=CliToApi().execute_by_audio,
            base_uri=self.base_uri,
            username=self.username,
            password=self.password)

        get_synapse_prs.add_argument('synapse_name',
                                     metavar="SYNAPSE_NAME",
                                     help="the synapse name")
        execute_by_name_prs.add_argument('synapse_name',
                                          metavar="SYNAPSE_NAME",
                                         help="the synapse name")
        execute_by_name_prs.add_argument('-v','--voice',
                                          help="output the audio",
                                          action="store_true")
        execute_by_name_prs.add_argument('-p','--parameters',
                                          metavar="PARAMETER_LIST",
                                          help="pass parameters to the synapse")
        execute_by_order_prs.add_argument('order',
                                          metavar="ORDER",
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

        parser.add_argument('-v', '--version', action='version',
                            version=pkg_resources.get_distribution('kalliope_rest').version)

        return parser

if __name__ == '__main__':
    pass
