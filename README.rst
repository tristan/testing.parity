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

1.0.3 (2018-09-24)
------------------
* Support Parity-Ethereum in version string

1.0.4 (2019-01-18)
------------------
* Support Parity versions >= 2.2.0

1.0.5 (2019-07-17)
------------------
* Update chainspec to support Constantinople EIPs

1.0.6 (2019-08-07)
------------------
* Allow enabling of websocket interface

1.0.7 (2019-10-19)
------------------
* Fix instantSeal engine for Parity versions >= 2.5.8
