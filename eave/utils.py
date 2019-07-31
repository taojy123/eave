import json
import re

from eave import *
import yaml


def find_resources(data, base_uri):
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
                

def find_target(data, target, excludes=None):
    excludes = excludes or []
    if isinstance(data, list):
        for item in data:
            if item in excludes:
                continue
            r = find_target(item, target, excludes)
            if r:
                return r
    elif isinstance(data, dict):
        if target in data:
            return data[target]
        else:
            for key, value in data.items():
                if key in excludes:
                    continue
                r = find_target(value, target, excludes)
                if r:
                    return r


def append_resource(doc, data, base_uri=''):
    for resource in find_resources(data, base_uri):
        api_uri = resource['uri']
        secured_by = resource.get('securedBy')
        
        for method_name, method_data in resource.items():
            if method_name not in ['get', 'post', 'put', 'patch', 'delete']:
                continue
            api = Api()
            name1 = resource.get('displayName', '')
            name2 = method_data.get('description', '')
            if name1 in name2:
                name1 = ''
            api.title = f'{name1} {name2}'.strip()
            api.uri = api_uri
            api.method = method_name

            secured_by = method_data.get('securedBy', secured_by)
            if secured_by:
                api.description = f'Secured By: **{secured_by}**'
            
            ups = re.findall(r'\{(.+)\}', api.uri)
            for up in ups:
                api.uri_params.append(UP(name=up))

            queryparameters = method_data.get('queryParameters', {})
            for p_name, p_data in queryparameters.items():
                p_data = p_data or {}
                p_data['name'] = p_name
                api.query_params.append(QP(p_data))
            
            properties = find_target(method_data.get('body'), 'properties') or {}
            for p_name, p_data in properties.items():
                p_data = p_data or {}
                p_data['name'] = p_name
                api.body_params.append(BP(p_data))
            
            api.body_example = find_target(method_data.get('body'), 'example', ['properties']) or ''
            api.response_example = find_target(method_data.get('responses'), 'example') or ''
            api.content_types = []
            
            doc.apis.append(api)
            
        append_resource(doc, resource, api_uri)
            
            
def raml2eave(raml_file, silence=True):
    
    raml_content = open(raml_file, encoding='utf8').read()
    data = yaml.safe_load(raml_content)
    
    if not silence:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    
    doc = Doc()
    doc.title = data.get('title', '')
    doc.version = data.get('version', '')
    doc.host = data.get('baseUri', '')
    doc.description = data.get('description', '')

    for note in data.get('documentation', []):
        doc.add_note(note)

    security_schemes = data.get('securitySchemes')
    for name, scheme in security_schemes.items():
        content = scheme.get('description', '')
        doc.add_note(title=name, content=content)

    append_resource(doc, data, '')
    
    return doc


# raml2eave('tiadmin.raml').build('tiadmin.html', 'zh')
# raml2eave('grs.raml').build('grs.html', 'zh')

