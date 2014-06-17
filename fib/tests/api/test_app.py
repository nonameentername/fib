import json
from unittest import TestCase
from webtest import TestApp

from fib.api.app import MAX_NUMBER_ALLOWED
from fib.api.app import application
from fib.api.app import calculate_fibonacci
from fib.api.app import get_fibonacci_sequence
from fib.api.app import validate_input


class TestValidateInput(TestCase):

    def test_validate_input_returns_false_for_non_number(self):
        self.assertEqual(validate_input(None)[0], False)
        self.assertEqual(validate_input('str')[0], False)

    def test_validate_input_returns_false_for_negative_number(self):
        self.assertEqual(validate_input('-1')[0], False)
        self.assertEqual(validate_input(-1)[0], False)

    def test_validate_input_returns_false_for_float_number(self):
        self.assertEqual(validate_input(1.7)[0], False)

    def test_validate_input_returns_false_when_n_is_too_large(self):
        self.assertEqual(validate_input(MAX_NUMBER_ALLOWED + 1)[0], False)

    def test_validate_input_returns_true_for_valid_numbers(self):
        self.assertEqual(validate_input(0)[0], True)
        self.assertEqual(validate_input('1')[0], True)
        self.assertEqual(validate_input('100')[0], True)
        self.assertEqual(validate_input(MAX_NUMBER_ALLOWED)[0], True)


class TestFibonacci(TestCase):

    def test_calculate_fibonacci_for_known_values(self):
        self.assertEqual(calculate_fibonacci(0), 0)
        self.assertEqual(calculate_fibonacci(1), 1)
        self.assertEqual(calculate_fibonacci(2), 1)
        self.assertEqual(calculate_fibonacci(3), 2)
        self.assertEqual(calculate_fibonacci(4), 3)

    def test_calculate_fibonacci_caches_value(self):
        cache = {}
        calculate_fibonacci(0, cache=cache)
        self.assertEqual(len(cache), 1)
        cached_value = cache[0]
        self.assertEqual(cached_value, 0)

    def test_get_fibonacci_sequence_for_known_values(self):
        self.assertEqual(get_fibonacci_sequence(5), [0, 1, 1, 2, 3])


class FunctionalTest(TestCase):

    def setUp(self):
        super(FunctionalTest, self).setUp()
        self.app = TestApp(application)

    def test_missing_resource_returns_not_found(self):
        response = self.app.get('/', status=404)
        message = json.loads(response.body)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            message['badRequest']['message'], 'resource was not found')
        self.assertEqual(message['badRequest']['code'], '404')

    def test_invalid_request_returns_error_message(self):
        response = self.app.get('/str', status=400)
        message = json.loads(response.body)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            message['badRequest']['message'],
            'n must be between 0 and {max_number}'.format(
                max_number=MAX_NUMBER_ALLOWED))
        self.assertEqual(message['badRequest']['code'], '400')

    def test_invalid_request_returns_bad_request(self):
        response = self.app.get('/str', status=400)
        self.assertEqual(response.status_code, 400)

        response = self.app.get('/-1', status=400)
        self.assertEqual(response.status_code, 400)

        response = self.app.get('/1.7', status=400)
        self.assertEqual(response.status_code, 400)

        response = self.app.get(
            '/{max_number}'.format(
                max_number=MAX_NUMBER_ALLOWED + 1), status=400)
        self.assertEqual(response.status_code, 400)

    def test_valid_request_returns__fibonacci_list(self):
        response = self.app.get('/5')
        self.assertEqual(response.status_code, 200)
        message = json.loads(response.body)
        self.assertEqual(message, [0, 1, 1, 2, 3])
