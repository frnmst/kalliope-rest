# api.py
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
import os
import sys
import appdirs
import pkg_resources
import json
from .api_exceptions import (AudioFileError,
                         AudioFileFormatError)
from .utils import (abstract_http_method,
                    perform_voice_output,
                    get_audio_file_mime)


# GET /
def get_kalliope_version(base_uri, username, password):
    """ Return Kalliope's version.
    """

    return abstract_http_method(lambda: requests.get(base_uri + "/",
                                     auth=(username, password)))
 # GET /synapses
def get_synapses(base_uri, username, password):
    """ Returns a list of all available synapses and their details.
    """

    return abstract_http_method(lambda: requests.get(base_uri + "/synapses",
                                     auth=(username, password)))

# GET /synapses/<synapse_name>
def get_synapse(base_uri, username, password, synapse_name):
    """ Returns the selected synapse and its details.
    """

    return abstract_http_method(lambda:
       requests.get(base_uri + "/synapses" + "/" + synapse_name,
                    auth=(username, password)))

# GET /mute
def get_listening_status(base_uri, username, password):
    """ Tells if Kalliope is ready to listen for vocal orders.
    """

    return abstract_http_method(lambda:
       requests.get(base_uri + "/mute",
                    auth=(username, password)))

# POST /synapses/start/id/<synapse_name>
def execute_by_name(base_uri, username, password, synapse_name, voice):
    """ Executes a synapse with the specified name.
    """

    payload = {'no_voice': perform_voice_output(voice)}
    return abstract_http_method(lambda:
           requests.post(base_uri + "/synapses/start/id" + "/" + synapse_name,
                             json=payload,
                             auth=(username, password)))

# POST /synapses/start/order
def execute_by_order(base_uri, username, password, order, voice):
    """ Execute the specified order by text.
    """

    payload = {'order': order, 'no_voice': perform_voice_output(voice)}
    return abstract_http_method(lambda:
           requests.post(base_uri + "/synapses/start/order",
                         json=payload,
                         auth=(username, password)))

# POST /synapses/start/audio
# Supported file types: WAV, MP3
def execute_by_audio(base_uri, username, password, audio_file, voice):
    """ Execute the specified order by audio.
    """

    try:
        mime_of_file = get_audio_file_mime(audio_file)
        # The audio file will be sent in binary mode, along with the mime type.
        files = {'file': (args.audio_file, open(audio_file, 'rb'),
             mime_of_file, {'Expires': '0'})}
        payload = {'no_voice': perform_voice_output(voice)}
        return abstract_http_method(lambda:
               requests.post(base_uri + "/synapses/start/audio",
                             files=files,
                             data=payload,
                             auth=(username, password)))
    except (IOError, FileNotFoundError):
        raise AudioFileError
    except AudioFileFormatError:
        raise

'''
# POST /mute
def set_mute_status(args):

    payload = {'mute': mute}
    return abstract_http_method(lambda:
           requests.post(base_uri + "/mute",
                         json=payload,
                         auth=(username, password)))
'''

if __name__ == '__main__':

    pass
