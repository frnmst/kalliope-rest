CLI Usage helps
===============

Main help
---------

    usage: kalliope_rest [-h] [-v] {kv,sps,sp,listening,exec} ...

    Kalliope REST API frontend

    positional arguments:
      {kv,sps,sp,listening,exec}
        kv                  Get the version of Kalliope
        sps                 Get all the synapses
        sp                  Get the selected synapse
        listening           tells if Kalliope is waiting for orders
        exec                Execute a synapse by different criterias

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit

    Return values: 0 OK, 1 API Error, 2 Invalid command

sps sub-command
---------------

    usage: kalliope_rest sps [-h]

    optional arguments:
      -h, --help    show this help message and exit

sp sub-command
--------------

    usage: kalliope_rest sp [-h] SYNAPSE_NAME

    positional arguments:
      SYNAPSE_NAME  the synapse name

    optional arguments:
      -h, --help    show this help message and exit

listening sub-command
---------------------

    usage: kalliope_rest listening [-h]

    optional arguments:
      -h, --help  show this help message and exit

exec sub-command
----------------

    usage: kalliope_rest exec [-h] {by-name,by-order,by-audio} ...

    positional arguments:
      {by-name,by-order,by-audio}

    optional arguments:
      -h, --help            show this help message and exit

exec by-name sub-command
------------------------

    usage: kalliope_rest exec by-name [-h] [-v] [-p PARAMETER_LIST] SYNAPSE_NAME

    positional arguments:
      SYNAPSE_NAME          the synapse name

    optional arguments:
      -h, --help            show this help message and exit
      -v, --voice           output the audio
      -p PARAMETER_LIST, --parameters PARAMETER_LIST
                            pass parameters to the synapse

exec by-order sub-command
-------------------------

    usage: kalliope_rest exec by-order [-h] [-v] ORDER_STRING

    positional arguments:
      ORDER_STRING  a textual version of the vocal order

    optional arguments:
      -h, --help    show this help message and exit
      -v, --voice   output the audio

exec by-audio sub-command
-------------------------

    usage: kalliope_rest exec by-audio [-h] [-v] FILE_NAME

    positional arguments:
      FILE_NAME    an audio file containing the vocal order

    optional arguments:
      -h, --help   show this help message and exit
      -v, --voice  output the audio


