from eave import *


doc = Doc(title='Test Api Document')
doc.host = 'http://www.apitest.com'
doc.description = """
this is a test document
- test1
- test2
"""


note1 = Note()
note1.title = 'test note1'
note1.content = """
this is the **first** test note
"""

note2 = Note()
note2.content = """
this is the **second** test note
```
{
    "a": 1,
    "b": 2 
}
```
"""

doc.notes = [note1, note2]


api1 = Api()
api1.title = "first api"
api1.method = "GET"
api1.uri = "/test1/<id>/"
api1.description = "this is the **first** api"

up1 = UriParam()
up1.name = 'id'
up1.description = 'resource id'
up1.example = 10
api1.uri_params = [up1]


qp1 = QueryParam()
qp1.name = 'page'
qp1.description = 'page number of list'
qp1.default = 1
api1.query_params = [qp1]



api2 = Api()
api2.title = "second api"
api2.method = "POST"
api2.uri = "/test2/"
api2.description = "this is the **second** api"

pp1 = PostParam(name='username', required=True)
pp2 = PostParam()
pp2.name = 'password'
pp2.required = True
api2.post_params = [pp1, pp2]
api2.body_example = """
{
    "username": "balabala",
    "password": "123456"
}
"""
api2.response_example = """
{
    "id": 2,
    "username": "balabala",
    "password": "123456"
}
"""

doc.apis = [api1, api2]


doc.add_api(
    title="thrid api 测测中文",
    method="DELETE",
    uri="/test3/",
    description="this is the **thrid** api 测测测中文",
    tips="""
##### test tips balabala...
```
print('hello world!')
```
"""
)



doc.build('test.html', language='zh')

jdata = doc.to_json()
open('test.json', 'w', encoding='utf8').write(jdata)

doc2 = Doc(jdata)
doc2.title += '2'
doc2.build('test2.html', 'zh')


