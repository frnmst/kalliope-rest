=============
kalliope-rest
=============

A CLI frontend and API for the Kalliope REST API

Examples
========

Command Line Interface example

::

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

Application Programming interface example

    >>> import kalliope_rest
    >>> print(kalliope_rest.get_kalliope_version('http://127.0.0.1:5000','admin','secret'))
    {
      "Kalliope version": "0.4.6"
    }


Documentation
=============

https://frnmst.gitlab.io/kalliope-rest

TODO
====

- Unit tests (in progress)
- New commands
    - New mute commands (in progress)
    - Ability to pass paramters to the exec by name subcommand
    - Ability to pass paramters as files (see 
      https://github.com/kalliope-project/kalliope/blob/master/Docs/rest_api.md#run-a-synapse-from-an-order specifically the accent-quotes example)
- PyPi package (in progress)
- Is there a possibility to encrypt this API?

Copyright and License
=====================

Copyright (c) 2017, Franco Masotti <franco.masotti@student.unife.it>

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

