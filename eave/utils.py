import json

import dnode
import requests
import os

import yaml

from eave import *

__all__ = ['auto_drf_apis', 'doc_from_openapi']


def _get_request(url, testhost=''):
    print('get:', testhost + url)
    if os.path.exists('eave_cache.json'):
        cache = open('eave_cache.json', encoding='utf8').read()
        cache = json.loads(cache)
    else:
        cache = {}
    if testhost:
        data = requests.get(testhost + url).json()
        cache[url] = data
        open('eave_cache.json', 'w', encoding='utf8').write(json.dumps(cache, indent=4))
        print('save cache')
    elif url in cache:
        data = cache[url]
        print('use cache')
    else:
        data = {}
        print('default empty')
    return data


def _action_description_handle(func):

    description = func.kwargs['description'] or ''
    assert description, f'{func.url_path} 接口缺少描述！请至少在 `__doc__` 中添加至少一行内容，作为接口名称。'

    method = list(func.mapping.keys())[0].upper()

    lines = description.strip().splitlines()
    title = lines[0].strip()
    result = {
        'title': title,
        'description': '',
        'query_params': [],
        'body_params': [],
        'response_description': '',
    }
    target = 'description'
    for line in lines[1:]:
        line = line.strip()
        if line in ['GET', 'POST', 'PUT', 'PATCH', 'PARAMS']:
            if method == 'GET':
                target = 'query_params'
            else:
                target = 'body_params'
            continue
        elif line == 'RESPONSE':
            target = 'response_description'
            continue
        
        if isinstance(result[target], str):
            result[target] += line + '\n\n'
        elif isinstance(result[target], list):
            name, description = line.split(':', 1)
            name = name.strip()
            description = description.strip()
            required = False
            default = ''
            if name.startswith('*'):
                name = name[1:]
                required = True
            if description.count('=>') == 1:
                description, default = description.split('=>')
            if target == 'query_params':
                item = QP(name=name, description=description, required=required, default=default)
            elif target == 'body_params':
                item = BP(name=name, description=description, required=required, default=default)
            else:
                assert False
            result[target].append(item)

    result['params'] = result['query_params'] + result['body_params']
    del result['query_params']
    del result['body_params']
    return result


def auto_drf_apis(res_name, url, view_set, testhost='http://127.0.0.1:8000'):
    """
    # todo: 加强这块文档和示例，写进 eave 主页介绍
    api_list, api_post, api_detail, actions = auto_drf_apis('用户', '/api/users/', UserViewSet)
    doc.add_apis(api_list, api_post, api_detail, *actions)
    """
    
    # ======= GET List =======
    api_list = Api()
    api_list.title = res_name + '列表'
    api_list.url = url
    api_list.method = 'GET'
    
    api_list.params = []
    if hasattr(view_set, 'filter_class'):
        filter_fields = view_set.filter_class.Meta.fields
        for field_name, kinds in filter_fields.items():
            for kind in kinds:
                query_name = f'{field_name}__{kind}'
                kind_zh = '筛选'
                if kind == 'exact':
                    kind_zh = '指定'
                    query_name = field_name
                elif kind in ['icontains', 'contains']:
                    kind_zh = '匹配'
                elif kind == 'in':
                    kind_zh = '命中'
                f = field_name.split('__')
                if len(f) == 1:
                    field_zh = view_set.serializer_class.Meta.model._meta.get_field(f[0]).verbose_name
                else:
                    q_model = view_set.serializer_class.Meta.model
                    for k in f[0:-1]:
                        q_model = q_model._meta.get_field(k).related_model
                    field_zh = q_model._meta.get_field(f[-1]).verbose_name
                description = kind_zh + field_zh
                api_list.params.append(QP(name=query_name, description=description))
    
    url = api_list.url
    data = _get_request(url, testhost)
    if len(data['results']) > 2:
        data['results'] = [data['results'][0]]
    api_list.response_example = json.dumps(data, ensure_ascii=False, indent=4)
    
    # ======= POST =======
    api_post = Api()
    api_post.title = '创建' + res_name
    api_post.url = url
    api_post.method = 'POST'
    
    serializer = view_set.serializer_class()
    api_post.params = []
    for field_name, field in serializer.fields.items():
        if field.read_only:
            continue
        type = 'string'
        field_type = str(field.__class__)
        if 'IntegerField' in field_type:
            type = 'integer'
        elif 'FloatField' in field_type:
            type = 'float'
        elif 'DecimalField' in field_type:
            type = 'decimal'
        elif 'BooleanField' in field_type:
            type = 'boolean'
        description = field.label
        if field.help_text:
            description += f' [{field.help_text}]'
        required = field.required
        default = field.default
        try:
            if 'empty' in str(default.__class__):
                default = view_set.serializer_class.Meta.model._meta.get_field(field_name).default
        except:
            # print(f'Warning: {field_name} field not found in {view_set.serializer_class.Meta.model}')
            pass
        api_post.params.append(BP(name=field_name, type=type, description=description, required=required, default=default))
    
    if data['results']:
        api_post.response_example = json.dumps(data['results'][0], ensure_ascii=False, indent=4)
    
    # ======= GET Detail =======
    api_detail = Api()
    api_detail.title = res_name + '详情'
    api_detail.url = f'{url.rstrip("/")}/<id>/'
    api_detail.method = 'GET'
    api_detail.params = [PP(name='id', description=f'{res_name} ID', example=1)]
    
    data = _get_request(url, testhost)
    if data['results']:
        res_id = data['results'][0].get('id')
        if res_id:
            url = f'{url.rstrip("/")}/{res_id}/'
        else:
            url = data['results'][0].get('url')
            items = url.split('/')[3:]
            url = '/' + '/'.join(items)
        data2 = _get_request(url, testhost)
        api_detail.response_example = json.dumps(data2, ensure_ascii=False, indent=4)
    
    # ======= Actions =======
    actions = []
    for item in dir(view_set):
        func = getattr(view_set, item)
        if not all([hasattr(func, 'detail'), hasattr(func, 'url_path'), hasattr(func, 'kwargs')]):
            continue
        detail = func.detail
        url_path = func.url_path
        description = func.kwargs['description']
        method = list(func.mapping.keys())[0].upper()
        result = _action_description_handle(func)
        if detail:
            action_url = f'{url.rstrip("/")}/<id>/{url_path}/'
        else:
            action_url = f'{url.rstrip("/")}/{url_path}/'
        api_action = Api(url=action_url, method=method, **result)
        actions.append(api_action)
    
    # ============================
    
    return api_list, api_post, api_detail, actions


class DNode(dnode.DNode):

    def __getattr__(self, item):
        if item not in self.fields:
            return None
        return super().__getattr__(item)


def doc_from_openapi(s):
    """
    [beta]
    make eave doc instance from a OpenAPI3 document
    s should be any of the following
    1. the url of openapi online, such as: http://some.domain.com/openapi.json or http://some.domain.com/openapi.yaml
    2. the file path of openapi document, such as: path/to/openapi.json or path/to/openapi.yaml
    3. the json string of openapi, such as: '{"openapi": "3.0.2", "paths": {...} }'
    4. the yaml string of openapi, such as: 'openapi: 3.0.2\npaths:\n  ...'
    5. the dict of parsed document, such as: {"openapi": "3.0.2", "paths": {...} }
    """

    if isinstance(s, dict):
        data = s
    else:
        assert isinstance(s, str), f's param must be dict or str, not {s}'

        if s.startswith('http'):
            url = s
            s = requests.get(url).text

        if os.path.isfile(s):
            s = open(s).read()

        if s.strip().startswith('{'):
            data = json.loads(s)
        else:
            data = yaml.safe_load(s)

    doc = Doc()
    root = DNode(data)

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

    paths = root.paths or {}
    for path, operations in paths.items():
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
            responses = operation.responses or {}

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
                # todo: support for $ref
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

            codes = list(responses.keys())
            if codes:
                if '200' in codes:
                    code = '200'
                else:
                    code = codes[0]

                response = responses[code]

                if 'content' in response:
                    # todo: improve real response example
                    api.response_example = json.dumps(response['content'], ensure_ascii=False, indent=4)

                api.response_description = response.get('description')

            doc.add_api(api)

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

    # doc.build('openapi.html', 'zh')
    return doc
