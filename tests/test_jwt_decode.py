import unittest

from craftai.jwt_decode import jwt_decode
from craftai.errors import CraftAiTokenError

JWT_IO_EXAMPLE="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ"

class TestJwtDecode(unittest.TestCase):

    def test_decode_works(self):
        (payload, signing_input, header, signature) = jwt_decode(JWT_IO_EXAMPLE)
        self.assertEqual(header, {
          "alg": "HS256",
          "typ": "JWT"
        })
        self.assertEqual(payload, {
          "sub": "1234567890",
          "name": "John Doe",
          "admin": True
        })

    def test_decode_fails_properly(self):
        self.assertRaises(
            CraftAiTokenError,
            jwt_decode,
            "not a jwt")
