'''Unittest case'''
import unittest
import bs4_based_parser
import params
import text


class TestParserDecoder(unittest.IsolatedAsyncioTestCase):
    '''Tests for the parser decoder'''
    # asyncSetUp method is overridden from the parent class
    # IsolatedAsyncioTestCase
    async def asyncSetUp(self):
        self.decoder = bs4_based_parser.decoder_str_to_params
        self.msgs = text.layouts['message_handler']['edit_params']

    # Each test method starts with the keyword test_
    async def test_decoder(self):
        '''Decode test'''
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
        result = await self.decoder(encrypted, self.msgs)
        self.assertEqual(result, decrypted)

    async def test_decoder_not_default_separator(self):
        '''Decode with not default separator test'''
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
        result = await self.decoder(encrypted, self.msgs, sep='$')
        self.assertEqual(result, decrypted)

    async def test_decoder_without_separator(self):
        '''Decode without separator test'''
        encrypted = 'text python'
        with self.assertRaises(AssertionError) as exc:
            await self.decoder(encrypted, self.msgs)
        self.assertEqual(
            exc.exception.args[0],
            # "Line 0 'text python' does not have a ' - ' separator!"
            self.msgs['no separator'].format(0, encrypted, ' - '))

    async def test_decoder_without_not_default_separator(self):
        '''Decode without not default separator test'''
        encrypted = 'text python'
        with self.assertRaises(AssertionError) as exc:
            await self.decoder(encrypted, self.msgs, sep='$')
        self.assertEqual(
            exc.exception.args[0],
            # "Line 0 'text python' does not have a '$' separator!"
            self.msgs['no separator'].format(0, encrypted, '$'))

        result = await self.decoder(encrypted, self.msgs, sep=' ')
        self.assertEqual(result, {'text': 'python'})


class TestParserPageDecoder(unittest.IsolatedAsyncioTestCase):
    '''Tests for the parser page decoder'''
    async def asyncSetUp(self):
        self.decoder = bs4_based_parser.decoder_str_to_page
        self.msgs = text.layouts['message_handler']['go_to_page']
        self.max_int = 10

    async def test_decoder(self):
        '''Decode '6':str to 5:int'''
        result = await self.decoder('6', self.msgs, self.max_int)
        self.assertEqual(result, 5)

    async def test_decoder_with_not_a_digit(self):
        '''Decode not a digit str to int'''
        with self.assertRaises(AssertionError) as exc:
            await self.decoder('text', self.msgs, self.max_int)
        self.assertEqual(
            exc.exception.args[0],
            self.msgs['not a digit'])

        with self.assertRaises(AssertionError) as exc:
            await self.decoder('O12', self.msgs, self.max_int)
        self.assertEqual(
            exc.exception.args[0],
            self.msgs['not a digit'])

    async def test_decoder_with_invalid_digit(self):
        '''Decode a invalid digit str to int'''
        with self.assertRaises(AssertionError) as exc:
            await self.decoder('0', self.msgs, self.max_int)
        self.assertEqual(
            exc.exception.args[0],
            self.msgs['invalid digit'].format(self.max_int))

        with self.assertRaises(AssertionError) as exc:
            await self.decoder('6', self.msgs, 3)
        self.assertEqual(
            exc.exception.args[0],
            self.msgs['invalid digit'].format(3))


class TestGetResponse(unittest.IsolatedAsyncioTestCase):
    '''Tests for the get response'''
    async def asyncSetUp(self):
        self.getter = bs4_based_parser.get_response
        self.kwargs = {'headers': {}, 'params': {}}

    async def test_empty_keyword_argument(self):
        '''Get response with empty keyword argument test'''
        with self.assertRaises(AssertionError) as exc:
            await self.getter(**self.kwargs)
        self.assertEqual(
            exc.exception.args[0],
            '''The 'url' keyword argument was not passed!''')

    async def test_response_wrong_content_type(self):
        '''Get response with wrong content type test'''
        self.kwargs.update(
            [('url', 'https://www.kymesonet.org/json/current/24H/ALBN.json'),
             ('headers', {'Accept': 'application/json',
                          'Content-Type': 'application/json',
                          'User-agent': 'py-parser/2.3'})]
        )
        with self.assertRaises(AssertionError) as exc:
            await self.getter(**self.kwargs)
        self.assertEqual(
            exc.exception.args[0],
            'Response has the wrong content-type!')


class TestParams(unittest.TestCase):
    '''Tests loading and unloading parameters'''

    def setUp(self):
        self.load = params.load_params
        self.unload = params.unload_params
        self.test_params = params.test
        self.logger = params.__name__
        self.old_data = self.load()
        self.unload({})

    def test_unload_params(self):
        '''Tests unloading parameters'''
        with self.assertLogs() as rec:
            self.unload(self.test_params)
        self.assertEqual(
            rec.output, [f'INFO:{self.logger}:unload_params() is running...'])

    def test_load_params(self):
        '''Tests loading parameters'''
        with self.assertLogs() as rec:
            self.load()
        self.assertEqual(
            rec.output, [f'INFO:{self.logger}:load_params() is running...'])

    def test_data_integrity(self):
        '''Tests data integrity'''
        data = {123: 'One hundred twenty three'}
        self.unload(data)
        self.assertEqual(self.load(), data)

    def tearDown(self):
        self.unload(self.old_data)


# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
