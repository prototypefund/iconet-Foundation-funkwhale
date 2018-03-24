import factory
import requests
import requests_http_signature

from funkwhale_api.factories import registry

from . import signing


registry.register(signing.get_key_pair, name='federation.KeyPair')


@registry.register(name='federation.SignatureAuth')
class SignatureAuthFactory(factory.Factory):
    algorithm = 'rsa-sha256'
    key = factory.LazyFunction(lambda: signing.get_key_pair()[0])
    key_id = factory.Faker('url')

    class Meta:
        model = requests_http_signature.HTTPSignatureAuth


@registry.register(name='federation.SignedRequest')
class SignedRequestFactory(factory.Factory):
    url = factory.Faker('url')
    method = 'get'
    auth = factory.SubFactory(SignatureAuthFactory)

    class Meta:
        model = requests.Request
