import base64
import hashlib
import json
import logging
from urllib.parse import quote_plus, urlencode
from uuid import uuid4

import requests
from Crypto.Cipher import DES3


class UrlBuilder(object):
    def __init__(
        self,
        domain="",
        path="",
        page="",
        secure=False,
        shorten_link=False,
        keep_trailing_slash=True,
        params=None,
    ):
        self._domain = domain
        self._path = [path] if path else []
        self._page = page
        self._params = [params] if params else []
        self._secure_link = secure
        self._shorten_link = shorten_link
        self._keep_trailing_slash = keep_trailing_slash

    def domain(self, domain):
        self._domain = domain
        return self

    def path(self, path):
        self._path.append(str(path))
        return self

    def page(self, page):
        self._page = str(page)
        return self

    def params(self, param):
        self._params.append(param)
        return self

    def secure(self):
        self._secure_link = True
        return self

    def shorten_link(self):
        self._shorten_link = True
        return self

    def build(self):
        if not self._domain:
            raise Exception("A domain is required to create a valid URL")
        url_prefix = "https" if self._secure_link else "http"

        if self._domain[-1] == "/":
            self._domain = self._domain[:-1]

        url_path = "/".join(self._path)
        if url_path and url_path[-1] != "/":
            url_path += "/"

        extracted_params = []
        if self._params:
            for param in self._params:
                if isinstance(param, dict):
                    for k, v in param.items():
                        extracted_params.append((str(k), str(v)))
                elif isinstance(param, tuple):
                    if len(param) > 2:
                        raise Exception("Tuple must follow structure (key, value)")
                    if len(param) == 1:
                        raise Exception(
                            "Parameter is missing value field in (key, value)"
                        )
                    extracted_params.append(param)
                else:
                    raise Exception(
                        "Parameters can only be passed in as a dict or tuple"
                    )
        params_str = ""
        if extracted_params:
            params_str = "?%s" % (urlencode(extracted_params, quote_via=quote_plus))

        url = "%s://%s/%s%s" % (url_prefix, self._domain, url_path, self._page)

        if not self._keep_trailing_slash and url[-1] == "/":
            url = url[0:-1]

        url = "%s%s" % (url, params_str)

        if self._shorten_link:
            raise NotImplemented
        return url


class PaymentHelpers:

    """this is the getKey function that generates an encryption Key for you by passing your Secret Key as a parameter."""

    def getKey(self, seckey):
        hashedseckey = hashlib.md5(seckey.encode("utf-8")).hexdigest()
        hashedseckeylast12 = hashedseckey[-12:]
        seckeyadjusted = seckey.replace("FLWSECK-", "")
        seckeyadjustedfirst12 = seckeyadjusted[:12]
        return seckeyadjustedfirst12 + hashedseckeylast12

    """This is the encryption function that encrypts your payload by passing the text and your encryption Key."""

    def encryptData(self, key, plainText):
        blockSize = 8
        padDiff = blockSize - (len(plainText) % blockSize)
        cipher = DES3.new(key, DES3.MODE_ECB)
        plaintext = "{}{}".format(plainText, "".join(chr(padDiff) * padDiff))
        encrypted = base64.b64encode(cipher.encrypt(str.encode(plaintext)))
        return encrypted.decode("ascii")


def generate_guid():
    return str(uuid4()).replace("-", "")


def make_request(method=None, url=None, params=None, data=None, **kwargs):
    try:
        headers = {"Content-Type": "application/json"}
        res = requests.request(
            method=method,
            url=url,
            data=json.dumps(data),
            headers=headers,
            params=params,
            **kwargs,
        )

        logging.info(f"Response from mNotify Response: {json.dumps(data)}")
        return res
    except Exception as e:
        logging.warn(e)
