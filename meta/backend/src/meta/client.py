import requests

from .exceptions import APIError


class API:

    def __init__(self, server='127.0.0.1:8000'):
        self.server = server

    def __getattr__(self, name):
        api_url = 'http://%s/api/%s/?json=true' % (self.server, name)

        def call(*args, **kwargs):
            api_args = requests.get(api_url).json()['args']
            params = { _['name']: _['default'] for _ in api_args}
            
            for i in range(len(args)):
                params[api_args[i]['name']] = args[i]

            params.update(kwargs)

            res = requests.post(api_url, json=params)
            try:
                result = res.json()
            except:
                print (res.text)
                raise

            if 200 <= res.status_code < 400:
                return result['result']

            if 400 <= res.status_code < 500:
                raise APIError(res.status_code, result['msg'], result['code'])

            raise result

        return call

