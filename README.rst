About
=====
``testing.parity`` automatically setups a parity instance, and destroys it after testing.

.. image:: https://travis-ci.org/tristan/testing.parity.svg?branch=master
   :target: https://travis-ci.org/tristan/testing.parity

.. image:: https://coveralls.io/repos/tristan/testing.parity/badge.png?branch=master
   :target: https://coveralls.io/r/tristan/testing.parity?branch=master

.. image:: https://codeclimate.com/github/tristan/testing.parity/badges/gpa.svg
   :target: https://codeclimate.com/github/tristan/testing.parity


Documentation
  https://github.com/tristan/testing.parity
Issues
  https://github.com/tristan/testing.parity/issues
Download
  https://pypi.python.org/pypi/testing.parity

Install
=======
Use pip::

   $ pip install testing.parity

And ``testing.parity`` requires ``parity`` server in your PATH.


Usage
=====
Create Parity instance using ``testing.parity.ParityServer``::

  import testing.parity
  import json
  import urllib.request

  # Lanuch new Parity-Ethereum server
  with testing.parity.ParityServer() as parity:
      # test that jsonrpc responds
      result = urllib.request.urlopen(
          urllib.request.Request(
              parity.url(),
              headers={'Content-Type': "application/json"},
              data=json.dumps({
                 "jsonrpc": "2.0",
                 "id": "1234",
                 "method": "eth_blockNumber",
                 "params": []
              }).encode('utf-8')
          ))
      print(json.load(result))

  # Parity server is terminated here


Requirements
============
* Python 2.7, 3.4, 3.5, 3.6

License
=======
Apache License 2.0


History
=======

1.0.1 (2018-08-03)
-------------------
* First release

1.0.2 (2018-08-06)
-------------------
* Added ``--min-gas-price`` option
