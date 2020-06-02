# TODO: Make class

from secrets import token_bytes

import Crypto.Cipher.AES

from my.utils.utils_3 import unmissing


class DecryptionFailed (Exception):
    pass


class CryptoManager:

    __slots__ = (
        'hash_module',
        'cipher_module',
        'mac_module',
        'token_bytes',
    )

    DEFAULT_MAC_MODULE = Crypto.Hash.HMAC
    DEFAULT_HASH_MODULE = Crypto.Hash.SHA256
    DEFAULT_CIPHER_MODULE = Crypto.Cipher.AES
    DEFAULT_TOKEN_BYTES = token_bytes

    def __init__(
            self, *,
            cipher_module=None,
            mac_module=None,
            hash_module=None,
            token_bytes=None,
    ):

        self.cipher_module = unmissing(
            cipher_module,
            self.DEFAULT_CIPHER_MODULE,
            missing=None,
        )

        self.hash_module = unmissing(
            hash_module,
            self.DEFAULT_HASH_MODULE,
            missing=None,
        )

        self.mac_module = unmissing(
            mac_module,
            self.DEFAULT_MAC_MODULE,
            missing=None,
        )

        self.token_bytes = unmissing(
            token_bytes,
            self.DEFAULT_TOKEN_BYTES,
            missing=None,
        )

    def hash(self, data, n=1):
        return self.hash_module.new(data if n <= 1 else self.hash(data, n - 1)).digest()

    def mac(self, key, data, n=0x86):

        return self.mac_module.new(
            key=key,
            msg=(data if n <= 1 else self.mac(key, data, n - 1)),
            digestmod=self.hash_module,
        ).digest()

    def encrypt(self, key, data):

        iv = self.rand_iv()
        th = self.hash(iv + data)

        return th + iv + self.cipher_module.new(
            key=self.hash(key),
            mode=self.cipher_module.MODE_CFB,
            IV=iv,
        ).encrypt(data)

    def decrypt(self, key, data):

        kh = self.hash(key)

        bs = self.cipher_module.block_size
        ks = len(kh)

        th = data[:ks]
        iv = data[ks:ks + bs]
        e = data[ks + bs:]

        d = self.cipher_module.new(
            key=kh,
            mode=self.cipher_module.MODE_CFB,
            IV=iv,
        ).decrypt(e)

        if self.hash(iv + d) != th:
            raise DecryptionFailed()

        return d

    def rand_iv(self, *, nbytes=None):

        nbytes = unmissing(nbytes, self.cipher_module.block_size, missing=None)

        return self.token_bytes(nbytes)

    pass


crypto_manager = CryptoManager()

########################################################################################################################
