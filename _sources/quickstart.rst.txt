Quickstart
==========

The first thing to do is to have a working instance of Kalliope, ready to 
execute orders. With these examples we wil assume that outr kalliope server
lies on the ``127.0.0.1`` address, listening on the port ``5000``. We will also 
assume to have ``admin`` and ``secret`` as credentials. You also need to enable 
the REST API on the server side.

Enabling the REST API
---------------------

To be able to run synapses using the API_, you need to enable ``CORS requests``
in your Kalliope configuration_ file.


.. _API: https://github.com/kalliope-project/kalliope/blob/master/Docs/rest_api.md

.. _configuration: https://github.com/kalliope-project/kalliope/blob/master/Docs/settings.md#rest-api


Using the CLI
-------------

You can use the CLI without installation

::

    $ git clone https://github.com/frnmst/kalliope_rest.git
    $ cd kalliope_rest
    $ python -m kalliope_rest

If you install the package you will get an executable file in the executables 
directory (for example /usr/bin), so you can call the program with

::

    $ kalliope_rest

Here are a couple of examples

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


Using the API
-------------

Once you download and install the library, the first thing to do is to import 
the module.

    >>> import kalliope_rest

We can then try the most basic method

    >>> kalliope_rest.get_kalliope_version('http://127.0.0.1:5000','admin','secret')
    {\n  "Kalliope version": "0.4.6"\n}\n'

A less confusing output would be

    >>> print(kalliope_rest.get_kalliope_version('http://127.0.0.1:5000','admin','secret'))
    {
      "Kalliope version": "0.4.6"
    }

Remember that this is JSON, so it can be parsed with the json module which is 
part of Python. In case you run one of the execute methods, not only the 
specified order will be executed, but you will also receive a response from 
the server. With some work you can also make your local computer speak the 
answer itself with, for example, espeak.

    >>> import json
    >>> from addict import Dict
    >>> import os
    >>> req = kalliope_rest.execute_by_order('http://127.0.0.1:5000','admin','secret',"ciao",False)
    >>> ans = Dict(json.loads(req))
    >>> speak = ans.matched_synapses[0].neuron_module_list[0].generated_message
    >>> os.system('espeak -v it "' + speak + '"')
