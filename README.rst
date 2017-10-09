=============
kalliope-rest
=============

A frontend for the Kalliope REST API

Note: This readme will serve as the program's documentation.

REST API
========

To be able to run synapses using the API_, you need to enable `CORS requests` in your 
Kalliope configuration_ file. 


.. _API: https://github.com/kalliope-project/kalliope/blob/master/Docs/rest_api.md

.. _configuration: https://github.com/kalliope-project/kalliope/blob/master/Docs/settings.md#rest-api

Installation
============

::

    # python setup.py install

Configuration File
==================

You will find the configuration file under

::

    ~/.config/kalliope_rest/kalliope_rest.conf

upon the first run of the script. What follows is
an example of configuration file which is included in
this repository

::

    [Network]
    Host = 127.0.0.1
    Port = 5000
      
    [Administration]
    Username = admin
    Password = secret

Examples
========

::

    $ kalliope_rest exec by-order "hello"

    {
        "matched_synapses": [
            {
                "matched_order": null,
                "neuron_module_list": [
                    {
                        "generated_message": "Bonjourmonsieur",
                        "neuron_name": "Say"
                    }
                ],
                "synapse_name": "say-hello-fr"
            }
        ],
        "status": "complete",
        "user_order": null
    }

    $ kalliope-rest exec by-audio "hello-command.wav" --voice

    {
        "matched_synapses": [
        {
          "matched_order": "Bonjour",
          "neuron_module_list": [
            {
              "generated_message": "Bonjour monsieur",
              "neuron_name": "Say"
            }
          ],
          "synapse_name": "say-hello-fr"
        }
      ],
      "status": "complete",
      "user_order": "bonjour"
    }


Help
====

Main help
---------

    usage: kalliope_rest [-h] [-v] {kv,sps,sp,exec} ...

    Kalliope REST API frontend

    positional arguments:
      {kv,sps,sp,exec}
        kv              Get the version of Kalliope
        sps             Get all the synapses
        sp              Get the selected synapse
        exec            Execute a synapse by different criterias

    optional arguments:
      -h, --help        show this help message and exit
      -v, --version     show program's version number and exit

    Return values: 0 OK, 1 API Error, 2 Invalid command

sp sub-command help
-------------------

    usage: kalliope_rest sp [-h] SYNAPSE_NAME

    positional arguments:
      SYNAPSE_NAME  the synapse name

    optional arguments:
      -h, --help    show this help message and exit

exec sub-command help
---------------------

    usage: kalliope_rest exec [-h] {by-name,by-order,by-audio} ...

    positional arguments:
      {by-name,by-order,by-audio}

    optional arguments:
      -h, --help            show this help message and exit

exec by-order sub-command help
------------------------------

    usage: kalliope_rest exec by-order [-h] [-v] ORDER_STRING

    positional arguments:
      ORDER_STRING  a textual version of the vocal order

    optional arguments:
      -h, --help    show this help message and exit
      -v, --voice   output the audio

exec by-name sub-command help
-----------------------------

    usage: kalliope_rest exec by-name [-h] [-v] [-p PARAMETER_LIST] SYNAPSE_NAME

    positional arguments:
      SYNAPSE_NAME          the synapse name

    optional arguments:
      -h, --help            show this help message and exit
      -v, --voice           output the audio
      -p PARAMETER_LIST, --parameters PARAMETER_LIST
                            pass parameters to the synapse

exec by-audio sub-command help
------------------------------

    usage: kalliope_rest exec by-audio [-h] [-v] FILE_NAME

    positional arguments:
      FILE_NAME    an audio file containing the vocal order

    optional arguments:
      -h, --help   show this help message and exit
      -v, --voice  output the audio


Dependencies
============

- Python 3.x
- Requests_
- python-magic_


.. _Requests: https://github.com/requests/requests/

.. _python-magic: https://github.com/ahupp/python-magic

Testing dependencies
--------------------

- requests-mock_
- pyfakefs_


.. _requests-mock: https://requests-mock.readthedocs.io/en/latest/

.. _pyfakefs: http://pyfakefs.org

Running the tests
=================

::

    $ python setup.py test

TODO
====

- Unit tests (in progress)
- New commands
    - New mute command
    - Ability to pass paramters to the exec by name subcommand
    - Ability to pass paramters as files (see 
      https://github.com/kalliope-project/kalliope/blob/master/Docs/rest_api.md#run-a-synapse-from-an-order specifically the accent-quotes example)
- PyPi package (in progress)
- Is there a possibility to encrypt this API?

Copyright and License
=====================

Copyright (c) 2017, Franco Masotti <franco.masotti@student.inife.it>

Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the "Software"), to deal 
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.

