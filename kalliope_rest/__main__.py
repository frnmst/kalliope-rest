#!/usr/bin/env python3

# __main__.py
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
import json
import sys
from .api_exceptions import (AudioFileError,
                             AudioFileFormatError)
from .cli_exceptions import ConfigurationParsingError
from .cli import CliInterface


def main(args=None):
    """ Call the CLI parser and handle all possible exception returned from the
        Kr class.
    """

    try:
        kr = CliInterface()
        args = kr.parser.parse_args()
        result = args.func(args)
        if result is not None:
            print(result)
        retcode = 0
    except ConfigurationParsingError:
        sys.stderr.write(str(e) + "\n")
        sys.stderr.write("Check your configuration file\n")
        retcode = 1
    except requests.exceptions.RequestException as e:
        sys.stderr.write("Requests error\n")
        sys.stderr.write(str(e) + "\n")
        retcode = 1
        # Inspired by https://stackoverflow.com/a/20725965
    except json.decoder.JSONDecodeError as e:
        # end of inspired by.
        sys.stderr.write("JSON decoder error (probably not a Kalliope server)\n")
        sys.stderr.write(str(e) + "\n")
        retcode = 1
    except AudioFileError as e:
        sys.stderr.write(str(e) + "\n")
        sys.stderr.write("File " + args.audio_file + " not found\n")
        retcode = 1
    except AudioFileFormatError as e:
        sys.stderr.write(str(e) + "\n")
        sys.stderr.write("Only WAV or MP3 files are compatible\n")
        retcode = 1
    sys.exit(retcode)


if __name__ == '__main__':

    main()
