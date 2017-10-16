# utils.py
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

# This module is directly linked with the api module only.

import requests
import magic
import os
import json
from .api_exceptions import (AudioFileError,
                             AudioFileFormatError)

def perform_voice_output(voice):

    if voice:
        return 'false'
    else:
        return 'true'

def abstract_http_method(requests_method):

    try:
        r = requests_method()
        json.loads(r.text)
        result = r.text
    except (requests.exceptions.RequestException, json.decoder.JSONDecodeError):
        raise
    return result

def get_audio_file_mime(audio_file):

    if not os.path.isfile(audio_file):
       raise FileNotFoundError
    mime_of_file = magic.from_file(audio_file, mime=True)
    if mime_of_file not in ['audio/wav', 'audio/x-wav', 'audio/mpeg3', 'audio/x-mpeg-3']:
       raise AudioFileFormatError("Provided audio file is not conforming to the format specifications")
    return mime_of_file

if __name__ == '__main__':

    pass
