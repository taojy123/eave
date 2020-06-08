import yaml
import json

y = """
openapi: 3.0.2
info:
  title: api docs
  version: ''
  description: 试试
paths:
  /tapp/products/:
    get:
      operationId: listProducts
      description: ''
      parameters:
      - name: page
        required: false
        in: query
        description: A page number within the paginated result set.
        schema:
          type: integer
      - name: page_size
        required: false
        in: query
        description: Number of results to return per page.
        schema:
          type: integer
      - name: id
        required: false
        in: query
        description: id
        schema:
          type: string
      - name: id__in
        required: false
        in: query
        description: id__in
        schema:
          type: string
      - name: name
        required: false
        in: query
        description: name
        schema:
          type: string
      - name: name__icontains
        required: false
        in: query
        description: name__icontains
        schema:
          type: string
      - name: price__lte
        required: false
        in: query
        description: price__lte
        schema:
          type: string
      - name: price__gte
        required: false
        in: query
        description: price__gte
        schema:
          type: string
      - name: order_by
        required: false
        in: query
        description: 排序
        schema:
          type: string
      - name: search
        required: false
        in: query
        description: A search term.
        schema:
          type: string
      - name: ordering
        required: false
        in: query
        description: Which field to use when ordering the results.
        schema:
          type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                type: object
                properties:
                  count:
                    type: integer
                    example: 123
                  next:
                    type: string
                    nullable: true
                  previous:
                    type: string
                    nullable: true
                  results:
                    type: array
                    items:
                      properties:
                        id:
                          type: integer
                          readOnly: true
                        name:
                          type: string
                          maxLength: 100
                        price:
                          type: integer
          description: ''
    post:
      operationId: createProduct
      description: ''
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              properties:
                name:
                  type: string
                  maxLength: 100
                price:
                  type: integer
          application/x-www-form-urlencoded:
            schema:
              properties:
                name:
                  type: string
                  maxLength: 100
                price:
                  type: integer
          multipart/form-data:
            schema:
              properties:
                name:
                  type: string
                  maxLength: 100
                price:
                  type: integer
      responses:
        '200':
          content:
            application/json:
              schema:
                properties:
                  id:
                    type: integer
                    readOnly: true
                  name:
                    type: string
                    maxLength: 100
                  price:
                    type: integer
          description: ''
  /tapp/products/{id}/:
    get:
      operationId: retrieveProduct
      description: ''
      parameters:
      - name: id
        in: path
        required: true
        description: A unique integer value identifying this product.
        schema:
          type: string
      - name: id
        required: false
        in: query
        description: id
        schema:
          type: string
      - name: id__in
        required: false
        in: query
        description: id__in
        schema:
          type: string
      - name: name
        required: false
        in: query
        description: name
        schema:
          type: string
      - name: name__icontains
        required: false
        in: query
        description: name__icontains
        schema:
          type: string
      - name: price__lte
        required: false
        in: query
        description: price__lte
        schema:
          type: string
      - name: price__gte
        required: false
        in: query
        description: price__gte
        schema:
          type: string
      - name: order_by
        required: false
        in: query
        description: 排序
        schema:
          type: string
      - name: search
        required: false
        in: query
        description: A search term.
        schema:
          type: string
      - name: ordering
        required: false
        in: query
        description: Which field to use when ordering the results.
        schema:
          type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                properties:
                  id:
                    type: integer
                    readOnly: true
                  name:
                    type: string
                    maxLength: 100
                  price:
                    type: integer
          description: ''
    put:
      operationId: updateProduct
      description: ''
      parameters:
      - name: id
        in: path
        required: true
        description: A unique integer value identifying this product.
        schema:
          type: string
      - name: id
        required: false
        in: query
        description: id
        schema:
          type: string
      - name: id__in
        required: false
        in: query
        description: id__in
        schema:
          type: string
      - name: name
        required: false
        in: query
        description: name
        schema:
          type: string
      - name: name__icontains
        required: false
        in: query
        description: name__icontains
        schema:
          type: string
      - name: price__lte
        required: false
        in: query
        description: price__lte
        schema:
          type: string
      - name: price__gte
        required: false
        in: query
        description: price__gte
        schema:
          type: string
      - name: order_by
        required: false
        in: query
        description: 排序
        schema:
          type: string
      - name: search
        required: false
        in: query
        description: A search term.
        schema:
          type: string
      - name: ordering
        required: false
        in: query
        description: Which field to use when ordering the results.
        schema:
          type: string
      requestBody:
        content:
          application/json:
            schema:
              properties:
                name:
                  type: string
                  maxLength: 100
                price:
                  type: integer
          application/x-www-form-urlencoded:
            schema:
              properties:
                name:
                  type: string
                  maxLength: 100
                price:
                  type: integer
          multipart/form-data:
            schema:
              properties:
                name:
                  type: string
                  maxLength: 100
                price:
                  type: integer
      responses:
        '200':
          content:
            application/json:
              schema:
                properties:
                  id:
                    type: integer
                    readOnly: true
                  name:
                    type: string
                    maxLength: 100
                  price:
                    type: integer
          description: ''
    patch:
      operationId: partial_updateProduct
      description: ''
      parameters:
      - name: id
        in: path
        required: true
        description: A unique integer value identifying this product.
        schema:
          type: string
      - name: id
        required: false
        in: query
        description: id
        schema:
          type: string
      - name: id__in
        required: false
        in: query
        description: id__in
        schema:
          type: string
      - name: name
        required: false
        in: query
        description: name
        schema:
          type: string
      - name: name__icontains
        required: false
        in: query
        description: name__icontains
        schema:
          type: string
      - name: price__lte
        required: false
        in: query
        description: price__lte
        schema:
          type: string
      - name: price__gte
        required: false
        in: query
        description: price__gte
        schema:
          type: string
      - name: order_by
        required: false
        in: query
        description: 排序
        schema:
          type: string
      - name: search
        required: false
        in: query
        description: A search term.
        schema:
          type: string
      - name: ordering
        required: false
        in: query
        description: Which field to use when ordering the results.
        schema:
          type: string
      requestBody:
        content:
          application/json:
            schema:
              properties:
                name:
                  type: string
                  maxLength: 100
                price:
                  type: integer
          application/x-www-form-urlencoded:
            schema:
              properties:
                name:
                  type: string
                  maxLength: 100
                price:
                  type: integer
          multipart/form-data:
            schema:
              properties:
                name:
                  type: string
                  maxLength: 100
                price:
                  type: integer
      responses:
        '200':
          content:
            application/json:
              schema:
                properties:
                  id:
                    type: integer
                    readOnly: true
                  name:
                    type: string
                    maxLength: 100
                  price:
                    type: integer
          description: ''
    delete:
      operationId: destroyProduct
      description: ''
      parameters:
      - name: id
        in: path
        required: true
        description: A unique integer value identifying this product.
        schema:
          type: string
      - name: id
        required: false
        in: query
        description: id
        schema:
          type: string
      - name: id__in
        required: false
        in: query
        description: id__in
        schema:
          type: string
      - name: name
        required: false
        in: query
        description: name
        schema:
          type: string
      - name: name__icontains
        required: false
        in: query
        description: name__icontains
        schema:
          type: string
      - name: price__lte
        required: false
        in: query
        description: price__lte
        schema:
          type: string
      - name: price__gte
        required: false
        in: query
        description: price__gte
        schema:
          type: string
      - name: order_by
        required: false
        in: query
        description: 排序
        schema:
          type: string
      - name: search
        required: false
        in: query
        description: A search term.
        schema:
          type: string
      - name: ordering
        required: false
        in: query
        description: Which field to use when ordering the results.
        schema:
          type: string
      responses:
        '204':
          description: ''
"""


data = yaml.safe_load(y)


import pprint
import dnode
from eave import *


class DNode(dnode.DNode):
    
    def __getattr__(self, item):
        if item not in self.fields:
            return None
        return super().__getattr__(item)


root = DNode(data)

doc = Doc()

info = root.info
if info:
    doc.title = info.title or ''
    doc.version = info.version or doc.version
    doc.description = info.description or ''


servers = root.servers
if servers:
    hosts = []
    for server in servers:
        h = server.url
        description = server.description
        if description:
            h += f'({description})'
        hosts.append(h)
    doc.host = ', '.join(hosts)

paths = root.paths
for path, operations in root.paths.items():
    print(path)
    for method, operation in operations.items():
        operation = DNode(operation)
        print(method)
        print(operation)

        api = Api()
        api.url = path
        api.title = operation.operationId
        api.description = operation.description
        api.method = method.upper()
        api.params = []
        api.content_types = []

        parameters = operation.parameters or []
        requestBody = operation.requestBody
        responses = operation.responses or []

        for parameter in parameters:
            category = parameter.get('in')
            name = parameter.name
            required = parameter.required or False
            description = parameter.description or ''

            # todo: support deprecated and allowEmptyValue
            deprecated = parameter.deprecated
            allowEmptyValue = parameter.allowEmptyValue

            type = 'string'
            example = ''
            schema = parameter.schema
            if schema:
                type = schema.type or type
                example = schema.example or example

            # in: "path", "query", "cookie", "header"
            p = None
            if category == 'path':
                p = PathParam()
            elif category == 'query':
                p = QueryParam()
                p.required = required
            elif category == 'cookie':
                # todo: support cookie parameters
                pass
            elif category == 'header':
                # todo: support header parameters
                pass

            if p:
                p.name = name
                p.description = description
                p.type = type
                p.example = example
                p.default = ''
                api.params.append(p)
                
        if requestBody and requestBody.content:
            param_names = []
            for content_type, value in requestBody.content.items():
                content = DNode(value)
                api.content_types.append(content_type)
                properties = content.schema and content.schema.properties or {}
                required_names = content.schema and content.schema.required or []
                for param_name, value in properties.items():
                    if param_name in param_names:
                        continue
                    param = DNode(value)
                    p = BodyParam()
                    p.name = param_name
                    p.type = param.type
                    p.description = param.description or ''
                    p.required = param_name in required_names
                    api.params.append(p)
                    param_names.append(param_name)
            
        api.make_body_example()
        
        # todo: support response
        response_description = ''
        response_example = ''
        
        doc.add_api(api)


doc.build('test.html', 'zh')


# todo: support more
# root.security
# root.externalDocs
# root.components
# root.components.schemas
# root.components.responses
# root.components.parameters
# root.components.examples
# root.components.requestBodies
# root.components.headers
# root.components.securitySchemes
# root.components.links
# root.components.callbacks


