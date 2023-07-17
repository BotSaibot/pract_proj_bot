import unittest
import bs4_based_parser


# Test cases to test Calulator methods
# You always create  a child class derived from unittest.TestCase
# class TestCalculator(unittest.TestCase):
#     # setUp method is overridden from the parent class TestCase
#     def setUp(self):
#         self.calculator = Calculator()

#     # Each test method starts with the keyword test_
#     def test_add(self):
#         self.assertEqual(self.calculator.add(4, 7), 11)

#     def test_subtract(self):
#         self.assertEqual(self.calculator.subtract(10, 5), 5)

#     def test_multiply(self):
#         self.assertEqual(self.calculator.multiply(3, 7), 21)

#     def test_divide(self):
#         self.assertEqual(self.calculator.divide(10, 2), 5)


class TestParserDecoder(unittest.IsolatedAsyncioTestCase):
    # asyncSetUp method is overridden from the parent class
    # IsolatedAsyncioTestCase
    async def asyncSetUp(self):
        self.decoder = bs4_based_parser.decoder_str_to_params

    # Each test method starts with the keyword test_
    async def test_decoder(self):
        encrypted = (
            'enable_snippets - False\nexperience - noExperience\nitems_on_page'
            ' - 2\norder_by - publication_time\nored_clusters - True\nprofessi'
            'onal_role - 96\nschedule - remote\nsearch_field - name, company_n'
            'ame, description\nstatus - non_archived\ntext - python')
        decrypted = {
            'enable_snippets': 'False',
            'experience': 'noExperience',
            'items_on_page': 2,
            'order_by': 'publication_time',
            'ored_clusters': 'True',
            'professional_role': 96,
            'schedule': 'remote',
            'search_field': ['name', 'company_name', 'description'],
            'status': 'non_archived',
            'text': 'python'
        }
        result = await self.decoder(encrypted)
        self.assertEqual(result, decrypted)

    async def test_decoder_not_default_separator(self):
        encrypted = (
            'enable_snippets$False\nexperience$noExperience\nitems_on_page'
            '$2\norder_by$publication_time\nored_clusters$True\nprofessi'
            'onal_role$96\nschedule$remote\nsearch_field$name, company_n'
            'ame, description\nstatus$non_archived\ntext$python')
        decrypted = {
            'enable_snippets': 'False',
            'experience': 'noExperience',
            'items_on_page': 2,
            'order_by': 'publication_time',
            'ored_clusters': 'True',
            'professional_role': 96,
            'schedule': 'remote',
            'search_field': ['name', 'company_name', 'description'],
            'status': 'non_archived',
            'text': 'python'
        }
        result = await self.decoder(encrypted, sep='$')
        self.assertEqual(result, decrypted)

    async def test_decoder_without_separator(self):
        encrypted = 'text python'
        with self.assertRaises(AssertionError) as cm:
            await self.decoder(encrypted)
        self.assertEqual(
            cm.exception.args[0],
            "Line 0 'text python' does not have a ' - ' separator!")

    async def test_decoder_without_not_default_separator(self):
        encrypted = 'text python'
        with self.assertRaises(AssertionError) as cm:
            await self.decoder(encrypted, sep='$')
        self.assertEqual(
            cm.exception.args[0],
            "Line 0 'text python' does not have a '$' separator!")

        result = await self.decoder(encrypted, sep=' ')
        self.assertEqual(result, {'text': 'python'})


class TestGetResponse(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.getter = bs4_based_parser.get_response
        self.kwargs = {'headers': {}, 'params': {}}

    async def test_empty_keyword_argument(self):
        with self.assertRaises(AssertionError) as cm:
            await self.getter(**self.kwargs)
        self.assertEqual(
            cm.exception.args[0],
            '''The 'url' keyword argument was not passed!''')

    async def test_response_wrong_content_type(self):
        self.kwargs.update(
            [('url', 'https://www.kymesonet.org/json/current/24H/ALBN.json'),
             ('headers', {'Accept': 'application/json',
                          'Content-Type': 'application/json',
                          'User-agent': 'py-parser/2.3'})]
        )
        with self.assertRaises(AssertionError) as cm:
            await self.getter(**self.kwargs)
        self.assertEqual(
            cm.exception.args[0],
            'Response has the wrong content-type!')


# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
