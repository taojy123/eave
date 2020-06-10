import unittest

from eave import Doc, Note, Api, PathParam, QueryParam, BodyParam


class TestDemo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_doc(self):
        doc = Doc(title='Test Api Document', version='v2')
        doc.host = 'http://www.apitest.com'
        doc.description = """
this is a test document
- test1
- test2
"""
        html = doc.build()
        self.assertIn('<h1>Test Api Document</h1>', html)
        self.assertIn('<li>Version: <code>v2</code></li>', html)
        self.assertIn('<li>Host: <code>http://www.apitest.com</code></li>', html)
        self.assertIn('<li>test1</li>', html)
        self.assertIn('<li>test2</li>', html)

    def test_note(self):
        doc = Doc()
        note1 = Note()
        note1.title = 'test note1'
        note1.content = 'This is the **first** test note'
        note2 = Note()
        note2.content = 'This note has no title'
        doc.add_note(note1)
        doc.add_note(note2)
        html = doc.build()
        self.assertIn('test note1', html)
        self.assertIn('This is the <strong>first</strong> test note', html)
        self.assertNotIn('note2', html)
        self.assertIn('This note has no title', html)

    def test_api(self):
        doc = Doc()
        api = Api()
        api.title = "first api"
        api.method = "GET"
        api.url = "/test1/<id>/"
        api.description = "this is the **first** api"
        doc.add_api(api)
        html = doc.build()
        self.assertIn('first api', html)
        self.assertIn('<div class="endpoint get">', html)
        self.assertIn('/test1/&lt;id&gt;/', html)
        self.assertNotIn('<id>', html)
        self.assertIn('<strong>first</strong>', html)

    def test_path_param(self):
        doc = Doc()
        api = Api(title='test api', url='/test/<id>/', method='GET')
        pp1 = PathParam()
        pp1.name = 'id'
        pp1.description = 'resource id'
        pp1.example = 10
        api.params.append(pp1)
        doc.add_api(api)
        html = doc.build()
        self.assertIn('<td><code>id</code></td>', html)
        self.assertIn('<td>resource id</td>', html)
        self.assertIn('<td>10</td>', html)

    def test_query_param(self):
        doc = Doc()
        api = Api(title='test api', url='/test/', method='GET')
        qp1 = QueryParam()
        qp1.name = 'page'
        qp1.description = 'page number of list'
        qp1.default = 1
        api.params.append(qp1)
        doc.add_api(api)
        html = doc.build()
        self.assertIn('<td><code>page</code></td>', html)
        self.assertIn('<td>page number of list</td>', html)
        self.assertIn('<td>1</td>', html)

    def test_body_param(self):
        doc = Doc()
        api = Api(title='test api', url='/test/', method='POST')
        bp1 = BodyParam(name='username')
        bp2 = BodyParam()
        bp2.name = 'password'
        api.params = [bp1, bp2]
        doc.add_api(api)
        html = doc.build()
        self.assertIn('<div class="endpoint post">', html)
        self.assertIn('<td><code>username</code></td>', html)
        self.assertIn('<td><code>password</code></td>', html)

    def test_body_example(self):
        doc = Doc()
        api = Api(title='test api', url='/test/', method='POST')
        api.body_example = """
{
    "username": "balabala",
    "password": "123456"
}
"""
        doc.add_api(api)
        html = doc.build()
        self.assertIn('"username": "balabala"', html)
        self.assertIn('"password": "123456"', html)

    def test_response_description(self):
        doc = Doc()
        api = Api(title='test api', url='/test/', method='POST')
        api.response_description = 'return *user* info'
        doc.add_api(api)
        html = doc.build()
        self.assertIn('return <em>user</em> info', html)

    def test_response_example(self):
        doc = Doc()
        api = Api(title='test api', url='/test/', method='POST')
        api.response_example = """
{
    "id": 2,
    "username": "balabala",
    "password": "123456"
}
"""
        doc.add_api(api)
        html = doc.build()
        self.assertIn('"id": 2', html)
        self.assertIn('"username": "balabala"', html)
        self.assertIn('"password": "123456"', html)

    def test_tips(self):
        doc = Doc()
        api = Api(title='test api', url='/test/', method='DELETE')
        api.tips = '## Be careful to destroy'
        doc.add_api(api)
        html = doc.build()
        self.assertIn('<div class="endpoint delete">', html)
        self.assertIn('<h2>Be careful to destroy</h2>', html)

    def test_language(self):
        doc = Doc()
        api = Api(title='test api', url='/test/', method='POST')
        api.body_example = '{}'
        doc.apis.append(api)
        html_en = doc.build()
        html_zh = doc.build(language='zh')
        self.assertIn('Contents', html_en)
        self.assertIn('Request Body Example', html_en)
        self.assertIn('Print This Document', html_en)
        self.assertIn('接口目录', html_zh)
        self.assertIn('示例请求数据', html_zh)
        self.assertIn('打印本文档', html_zh)


if __name__ == '__main__':
    unittest.main(verbosity=1)




