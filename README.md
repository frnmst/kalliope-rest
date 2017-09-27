# kalliope-rest

A frontend for the Kalliope REST API

## REST API

See https://github.com/kalliope-project/kalliope/blob/master/Docs/rest_api.md

To be able to run synapses, you need to enable `CORS requests`. See 
https://github.com/kalliope-project/kalliope/blob/master/Docs/settings.md#rest-api

## Help

```
usage: kalrest.py [-h] {kv,sps,sp,exec} ...

Kalliope REST API frontend

positional arguments:
  {kv,sps,sp,exec}
    kv              Get the version of Kalliope
    sps             Get all the synapses
    sp              Get the selected synapse
    exec            Execute a synapse by different criterias

optional arguments:
  -h, --help        show this help message and exit
```

## Dependencies

- Python 3.x
- [Requests](https://github.com/requests/requests/)
- [python-magic](https://github.com/ahupp/python-magic)

## TODO

- Full coverage of HTTP response checks
- Handle all possible exceptions
- Unit tests
- Documentation
- PyPi package

## Copyright and License

Copyright (c) 2017, Franco Masotti

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

