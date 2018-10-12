import re
import logging

from requests.auth import AuthBase

_logger = logging.getLogger(__name__)


class HttpBearerAuth(AuthBase):
    def __init__(self, username=None, password=None):
        self._tokens = {}
        if username is not None and password is not None:
            self._auth_info = (username, password)

    def _retry_using_http_Bearer_auth(self, response, **kwargs):
        if 'Authorization' in response.request.headers:
            return response

        params = dict(re.findall('(\w+)="([^"]+)",?', response.headers['WWW-Authenticate'][7:]))
        token_key = '{realm}-{service}-{scope}'.format(**params)
        error = params.pop('error', None)
        realm = params.pop('realm')
        history = [response]

        if error:
            _logger.debug('Not retrying authentication: Bearer auth previously failed with error: {}'.format(error))
            return response

        if token_key not in self._tokens:
            _logger.debug('Requesting token from {} with scope {}'.format(realm, params['scope']))

            content_length = int(response.request.headers.get('Content-Length', '0'), base=10)
            if hasattr(response.request.body, 'seek'):
                if content_length > 0:
                    response.request.body.seek(-content_length, 1)
                else:
                    response.request.body.seek(0, 0)

            response.content
            response.raw.release_conn()
            token_request = response.request.copy()
            token_request.prepare_url(realm, params=params)
            token_request.prepare_auth(auth=self._auth_info)

            kwargs_nostream = dict(kwargs, stream=False)
            token_response = response.connection.send(token_request, **kwargs_nostream)

            if token_response.status_code == 200:
                self._tokens[token_key] = token_response.json()['token']
                history.append(token_response)
            else:
                token_response.history.append(response)
                return token_response

        authd_request = response.request.copy()
        authd_request.headers['Authorization'] = 'Bearer {}'.format(self._tokens[token_key])
        authd_response = response.connection.send(authd_request, **kwargs)
        authd_response.history += history

        return authd_response

    def _response_hook(self, r, **kwargs):
        if r.status_code == 401:
            if r.headers.get('WWW-Authenticate', '').startswith('Bearer'):
                return self._retry_using_http_Bearer_auth(r, **kwargs)

    def __call__(self, r):
        r.headers['Connection'] = 'Keep-Alive'
        r.register_hook('response', self._response_hook)
        return r
