# ======= Basic Usage ========

# import components of eave
from eave import Doc, Note, Api, UP, QP, PP

# or you can import all
from eave import *


# startup a new doc
doc = Doc(title='My Api Document', host='www.myapi.com')

# add description for the doc
doc.description = """
the content of description is **markdown** format
1. one point
2. two point
3. three point
"""

# add a note into the doc
doc.add_note(
    title="note title",
    content="the content of note is also **markdown** format"
)

# add a get api into the doc
doc.add_api(
    title='Get all orders of shop',
    uri='/shop/<id>/orders/',
    method='GET',
    description='Get all orders of shop, shop admin login required',
    uri_params=[
        UP(name='id', description='the id of shop')
    ],
    query_params=[
        QP(name='page', type='integer', default=1),
        QP(name='page_size', type='integer', default=10),
    ],
    response_example="""
{
    "page": 1,
    "page_size": 10,
    "data": [
        {
          "order_id": "0021",
          "order_price": "120.00",
          "order_name": "xxx1",
        }
    ]
}
"""
)

# add a post api into the doc
doc.add_api(
    title='Create a product',
    uri='/products/',
    method='POST',
    post_params=[
        PP(name='name', required=True),
        PP(name='category', example='food'),
        PP(name='price', type='float', default=0),
    ],
    content_types=['application/json'],
    body_example="""
{
    "name": "Sprite 250ml",
    "category": "food",
    "price": 3.5
}
""",
    tips="""some `tips` for this api, also **markdown** format"""
)

# build the document to html
doc.build('best.html')



# ========= Advanced Usage =========

# export to json
json_data = doc.to_json()

# create doc by json
doc2 = Doc(json_data)
doc2.title = 'My Second Api Document'

# build by chinese language
doc2.build('best2.html', language='zh')

# export to yaml
yaml_data = doc.to_yaml()
doc3 = Doc(yaml_data)
doc3.build('best3.html')
