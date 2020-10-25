import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'thegux.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'fullProject'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def validate_auth_header(auth_header):
    splitted_header = auth_header.split()
    bearer_part = splitted_header[0]
    valid_auth = True
    if len(splitted_header) != 2:
        valid_auth = False
    if bearer_part.lower() != "bearer":
        valid_auth = False
    return valid_auth


def get_token():
    headers = request.headers
    if 'Authorization' in request.headers:
        auth_header = headers['Authorization']
        valid_header = validate_auth_header(auth_header)
        if not valid_header:
            print("INVALID")
            raise AuthError({
                'status': 401,
                'message': 'Unauthorized'
            }, status_code=401)
        token = auth_header.split()[1]
        return token
    raise AuthError({
        'status': 401,
        'message': 'Unauthorized'
    }, status_code=401)


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid header',
            'description': 'Authorization malformed.',
            'status': 401,
            'message': 'invalid jwt token'
        }, status_code=401)

    public_keys_url = f' https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    try:
        response = request.get(public_keys_url)
        jwks = response.json() if response.status_code == 200 else None
    except:
        raise AuthError({
            'code': 'invalid header',
            'description': 'Not Authorized.',
            'status': 401,
            'message': 'invalid jwt token'
        }, status_code=401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e'],
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claim',
                'description': 'Invalid Claim. Please, verify the audience.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_headers',
                'description': 'Sorry, we were unable to parse the authentication token provided.'
            }, 401)
    raise AuthError({'code': 'invalid_header',
                     'description': 'Unable to find the appropriate key.'}, 401)

    raise Exception('Not Implemented')


def check_permissions(permission, jwt_payload):
    jwt_has_permissions = 'permissions' in jwt_payload
    if not jwt_has_permissions or (jwt_has_permissions and permission not in jwt_payload['permissions']):
        raise AuthError({
            'code': 'unauthorized',
            'description': 'you dnn\'t have permissions to view this resource .'
        }, 401)
    return True


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token()
            try:
                payload = verify_decode_jwt(token)
            except:
                raise AuthError({
                    'code': 'invalid token',
                    'description': 'Token could not be verified, please try again.'
                }, 401)
            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
