import json
import re

from eave import *
import yaml


def find_resource(data, base_uri):
    for key, value in data.items():
        if not key.startswith('/'):
            continue
        if not isinstance(value, dict):
            continue
        for method in ['get', 'post', 'put', 'patch', 'delete']:
            if method in value:
                resource = value
                resource['uri'] = base_uri + key
                yield resource
                break
                

def find_target(data, target):
    if isinstance(data, list):
        for item in data:
            r = find_target(item, target)
            if r:
                return r
    elif isinstance(data, dict):
        if target in data:
            return data[target]
        else:
            for value in data.values():
                r = find_target(value, target)
                if r:
                    return r


def append_resource(doc, data, base_uri=''):
    for resource in find_resource(data, base_uri):
        for method_name, method in resource.items():
            if method_name not in ['get', 'post', 'put', 'patch', 'delete']:
                continue
            api = Api()
            api.title = resource.get('displayName') + method.get('description')
            api.uri = resource['uri']
            api.method = method_name
            
            ups = re.findall(r'\{(.+)\}', api.uri)
            for up in ups:
                api.uri_params.append(UP(name=up))

            queryparameters = method.get('queryParameters', {})
            for p_name, p_data in queryparameters.items():
                p_data = p_data or {}
                p_data['name'] = p_name
                api.query_params.append(QP(p_data))
            
            properties = find_target(method.get('body'), 'properties') or {}
            for p_name, p_data in properties.items():
                p_data = p_data or {}
                p_data['name'] = p_name
                api.post_params.append(PP(p_data))
            
            api.body_example = find_target(method.get('body'), 'example') or ''
            api.response_example = find_target(method.get('responses'), 'example') or ''
            api.content_types = []
            
            doc.apis.append(api)
            
            append_resource(doc, method, api.uri)
            
            
raml_content = open('api.raml', encoding='utf8').read()

data = yaml.safe_load(raml_content)

print(json.dumps(data, ensure_ascii=False, indent=2))


doc = Doc()
doc.title = data.get('title', '')
doc.version = data.get('version', '')
doc.host = data.get('baseUri', '')
doc.description = data.get('description', '')

for note in data.get('documentation', []):
    doc.add_note(note)

append_resource(doc, data, '')
        
        
doc.build('api.html', 'zh')

