import testing.parity
import unittest
import json
import urllib.request
import time
import os

class TestParity(unittest.TestCase):
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

    def test_send_transactions(self):
        try:
            parity = testing.parity.ParityServer(
                network_id=0x42,
                enable_ws=True,
                min_gas_price=10000000000,
                faucet_private_key=b'}\x82Cl\xbc\x8bc\x8f-\xf9V\xfct{W\\\xdb6D\xf8\x13w\x87\x95\xf6\x8a\x97\x04\x9c\xb8\x0fk')
            address = "0xf0fd3db9396b084d26d4f838eade9f111a715a29"

            txs = [
                ("0xc337816fd40c6a54f77a1445fa1ea6ab5101294974515312052b670650e2aca9", "0xf8718310000085028fa6ae0082520894000000000000000000000000000000000000000089056bc75e2d631000008081a8a0e0e959ccf4b4baf9b32dda1c210a321e71af96b5f66269fb2beb38298f89e5e8a0207b860442764f685024479d57c99a2c91fcd5b204eb2c728a98320dc9db04a5"),
                ("0x60b9b36033d99d36b52ff94d033f2d99ff1bf15c5c848d8af9b8295c3d19fbd7", "0xf8718310000185028fa6ae0082520894000000000000000000000000000000000000000089056bc75e2d631000008081a8a021025e7ddc5ad4744c2dfeffa84fdddaaa64e9f4681657c731e3cc020b3f9592a00f42710314e49d47c66aa63003d6820cdfc59c72c7a8037cbce5024b81ebaa1a"),
                ("0xc849b5f7e6b73d531aa4381646cb3b25871efcc5287c879f834a2e036e409938", "0xf8718310000285028fa6ae0082520894000000000000000000000000000000000000000089056bc75e2d631000008081a8a06391c32a10f084529e42a2b992f0da95994fcace83e99735765cc758c0d137ffa018683b0cd87c7d231004608e11b81841992b0b5b47e8ea7f31c9e5653d2f0c90"),
                ("0x7e1388c57e625c824902dd8a61e06679d74265d7451b4cd1f3f4be0c2ccd5473", "0xf8718310000385028fa6ae0082520894000000000000000000000000000000000000000089056bc75e2d631000008081a8a0eb6b075192aadbc0899c57fb86ed0cf11709dd116344ea8dd9990c4e81320d62a072798f2facc4b0cb30e65cd429c6aabfed654d9817e85b52021bfdbeea8a2bd5"),
                ("0x3b88fddb61a52e80bc8141354bb9cf1445c6b3fbf3ac2a2421c2af3f61741f21", "0xf8718310000485028fa6ae0082520894000000000000000000000000000000000000000089056bc75e2d631000008081a8a08eed90177f77ef1ae1c943522c496f26ed71c0c3e7a54f4bfea9ea1a7eff635ea07d73fa41256f5727694bec32fd2da0046ad804654af26746d61719ff26ccaa5f"),
                ("0x6483459e4be0559f8758b9179b81ae8730406b3c15d36dcab2e14184fd112f7e", "0xf8718310000585028fa6ae0082520894000000000000000000000000000000000000000089056bc75e2d631000008081a8a07435f4729015dbb6c70a8d5d65a19aef73ca3017e3520c5aec1ab8b563ab5585a05a9928ff026a1a1fc9e05d8e6df7c7ae938c6622a8b7daffcb263fe9c99bfd2c"),
                ("0x82d696e461d9da1fc1a15d4e832034172a6ba6256789f8180f4d2efed8fff22e", "0xf8718310000685028fa6ae0082520894000000000000000000000000000000000000000089056bc75e2d631000008081a8a0f58ef89a4f5a09713a6a1d9d06c17e243e50ec609533f9e68600e063526291f6a00b530d5f9651b01c62d03dd34319827f58bdc9adb790a9591ded8ccc15e4aae6"),
                ("0x72a95fb830d413a3e2e2a2ed8eab85012da8eedc80ef2e6e29b81125a701ecaf", "0xf8718310000785028fa6ae0082520894000000000000000000000000000000000000000089056bc75e2d631000008081a8a02ab3f214bdd73b3e0b63487a9108b6412d66f406f1ef7e34bf1ecec89799c97da0760ac31516d28025a2ea2410b1fc5f2e2613cda70ff3861e696b871c05b8dbcf"),
                ("0xa39670d948e05a67f78ca2f9b560e136c93a786537093c9bd780695d2b31b24a", "0xf8718310000885028fa6ae0082520894000000000000000000000000000000000000000089056bc75e2d631000008081a7a09f4aa314d0a1b70bffd9448be2bcc79591fa8bcc54219e414e85773315341b96a063be68037a3b5f066db3affc54167edb0d963d20bba6501fa12e0c32e51642f6"),
                ("0xb9491f2876689953c08f62d5f9e56a4ee4fe56db140df285a6da9166f051f992", "0xf8718310000985028fa6ae0082520894000000000000000000000000000000000000000089056bc75e2d631000008081a7a02d2c4480889a5afc0cdf671bd3eee85c2a8553cb9ce45e48e5b380098c20f515a068cc79a5b6a0d097364b8faa21280a5fb6b07af2e4073d28360e666c78a7bbff")
            ]

            for i, tx in enumerate(txs):
                expected_hash, raw_tx = tx

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
                block_number = int(json.load(result)['result'], 16)
                assert block_number == i

                result = urllib.request.urlopen(
                    urllib.request.Request(
                        parity.url(),
                        headers={'Content-Type': "application/json"},
                        data=json.dumps({
                            "jsonrpc": "2.0",
                            "id": "1234",
                            "method": "eth_getTransactionCount",
                            "params": [address]
                        }).encode('utf-8')
                    ))
                nonce = int(json.load(result)['result'], 16)
                assert nonce == 0x100000 + i

                result = urllib.request.urlopen(
                    urllib.request.Request(
                        parity.url(),
                        headers={'Content-Type': "application/json"},
                        data=json.dumps({
                            "jsonrpc": "2.0",
                            "id": "1234",
                            "method": "eth_sendRawTransaction",
                            "params": [raw_tx]
                        }).encode('utf-8')
                    ))
                tx_hash = json.load(result)['result']
                assert tx_hash == expected_hash
                start = time.time()
                while True:
                    result = urllib.request.urlopen(
                        urllib.request.Request(
                            parity.url(),
                            headers={'Content-Type': "application/json"},
                            data=json.dumps({
                                "jsonrpc": "2.0",
                                "id": "1234",
                                "method": "eth_getTransactionByHash",
                                "params": [tx_hash]
                            }).encode('utf-8')
                        ))
                    receipt = json.load(result)['result']
                    if receipt is not None and receipt['blockNumber'] is not None:
                        assert int(receipt['blockNumber'], 16) == block_number + 1
                        break
                    elif receipt is not None:
                        assert int(receipt['nonce'], 16) == nonce
                        print(receipt)
                    if time.time() - start > 5.0:
                        assert False, "timeout at tx: #{} {}".format(i, tx_hash)
                    time.sleep(0.5)
        finally:
            parity.stop()
