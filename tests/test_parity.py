import testing.parity
import unittest
import json
import urllib.request
import time
import os

class TestPostgresql(unittest.TestCase):
    def test_basic(self):
        try:
            # start postgresql server
            parity = testing.parity.ParityServer(network_id=42)
            self.assertIsNotNone(parity)
            params = parity.dsn()
            self.assertEqual('http://localhost:{}'.format(parity.settings['jsonrpc_port']), params['url'])
            self.assertEqual('http://localhost:{}'.format(parity.settings['jsonrpc_port']), parity.url())
            self.assertEqual(42, params['network_id'])
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
            self.assertEqual(json.load(result)['result'], '0x0')

            result = urllib.request.urlopen(
                urllib.request.Request(
                    parity.url(),
                    headers={'Content-Type': "application/json"},
                    data=json.dumps({
                        "jsonrpc": "2.0",
                        "id": "1234",
                        "method": "net_version",
                        "params": []
                    }).encode('utf-8')
                ))
            self.assertEqual(json.load(result)['result'], str(42))

        finally:
            # shutting down
            pid = parity.server_pid
            self.assertTrue(parity.is_alive())

            parity.stop()
            time.sleep(1)

            self.assertFalse(parity.is_alive())
            with self.assertRaises(OSError):
                os.kill(pid, 0) # process is down
