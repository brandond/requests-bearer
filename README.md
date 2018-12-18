requests-bearer
===============

[![image](https://badge.fury.io/py/requests-bearer.svg)](https://badge.fury.io/py/requests-bearer)
[![image](https://travis-ci.com/brandond/requests-bearer.svg?branch=master)](https://travis-ci.com/brandond/requests-bearer)

An implementation of JSON Web Tokens using the Bearer authentication scheme for Requests.

Specifically, this implementation is compliant with the JWT schema adopted by the Docker v2 Registry service, wherein the Realm indicates a URI at which a token can be obtained.

Usage
-----

```python
import requests
from requests_bearer import HttpBearerAuth

r = requests.get('https://index.docker.io/v2/library/_/python/tags/list', auth=HttpBearerAuth('username', 'password'))
```

Options
-------

  - `username`: Username.  
    Default: None

  - `password`: Password.  
    Default: None

If a username and password are provided, the client authenticates to the token server using Basic authentication. If username and password are not specified, an attempt is made to obtain a token anonymously.
