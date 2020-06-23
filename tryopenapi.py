
import json

import yaml
import dnode
from eave import *

openapi_yaml = open('openapi.yaml').read()
openapi_json = open('openapi.json').read()

yaml_data = yaml.safe_load(openapi_yaml)
json_data = json.loads(openapi_json)

assert yaml_data == json_data

class DNode(dnode.DNode):
    
    def __getattr__(self, item):
        if item not in self.fields:
            return None
        return super().__getattr__(item)


root = DNode(json_data)

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
    # print(path)
    for method, operation in operations.items():
        operation = DNode(operation)
        # print(method)
        # print(operation)

        api = Api()
        api.url = path
        api.title = operation.summary or operation.description or operation.operationId
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


doc.build('openapi.html', 'zh')


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


