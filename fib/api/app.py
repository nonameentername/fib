import json
from bottle import default_app
from bottle import get
from bottle import response
from bottle import route
from bottle import run
from functools import wraps


MAX_NUMBER_ALLOWED = 1000


def cache_fibonacci(f):
    """ This method decorator caches the result of an annotated method.
    It takes as arguments a number and cache keyword argument.
    It intercepts the method call and stores the response in the cache.
    When a value is found in the cache it uses that instead of calling f
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        number = args[0]

        if 'cache' in kwargs and kwargs['cache'] is not None:
            cache = kwargs['cache']

            if number in cache:
                return cache[number]
            else:
                result = f(*args, **kwargs)
                cache[number] = result
                return result

        result = f(*args, **kwargs)
        return result
    return wrapper


@cache_fibonacci
def calculate_fibonacci(number, cache=None):
    """ This method returns the Fibonacci number for nth position
    :param number: int number used to calculate Fibonacci
    :param cache: dict used to cache the values of Fibonacci
    """
    if number == 0 or number == 1:
        return number

    return (calculate_fibonacci(number - 2, cache=cache) +
            calculate_fibonacci(number - 1, cache=cache))


def get_fibonacci_sequence(number):
    """ This method returns the first n Fibonacci numbers starting from 0
    :param number: int number used to calculate list of Fibonacci numbers
    """
    result = []
    cache = {}
    for i in range(0, number):
        result.append(calculate_fibonacci(i, cache=cache))

    return result


def handle_bad_request():
    """ This method builds a response for an invalid request """
    response.status = 400
    result = {'badRequest': {
        'code': '400',
        'message': 'n must be between 0 and {max_number}'.format(
            max_number=MAX_NUMBER_ALLOWED)}}
    return json.dumps(result)


def handle_not_found():
    """ This method builds a response for an invalid request """
    response.status = 404
    result = {'badRequest': {
        'code': '404',
        'message': 'resource was not found'}}
    return json.dumps(result)


def validate_input(number):
    """ This method validates the request input
    :param number: argument to validate
    returns a tuple: first argument returns if the request is valid
    second argument contains the error response when invalid
    """
    try:
        float_number = float(number)
        int_number = int(number)

        if float(int_number) != float_number:
            return False, handle_bad_request()

    except:
        return False, handle_bad_request()

    if int_number < 0:
        return False, handle_bad_request()

    if int_number > MAX_NUMBER_ALLOWED:
        return False, handle_bad_request()

    return True, None


@get('/<number>')
def fibonacci(number):
    """ bottle request route for Fibonacci service
    :param number: value used to calculate Fibonacci
    This method sets the response headers and status code and
    returns the response body
    """
    response.headers['Content-Type'] = 'application/json'

    valid, message = validate_input(number)
    if not valid:
        return message

    return json.dumps(get_fibonacci_sequence(int(number)))


@route("/")
@route("/<url:re:.+>")
def not_found(url=None):
    """ bottle request route for invalid urls
    returns not found status code and error message
    :param url: url route for request
    """
    response.headers['Content-Type'] = 'application/json'
    return handle_not_found()


if __name__ == "__main__":
    run(host='0.0.0.0', port=8080, reloader=True, server='paste')
else:
    application = default_app()
