# python3

import os
import sys
import json
import mistune

from .step import Template


__all__ = ['Doc', 'Note', 'Api', 'Param', 'UriParam', 'QueryParam', 'PostParam', 'UP', 'QP', 'PP']


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STYLE = open(os.path.join(BASE_DIR, 'resource/style.css'), encoding='utf8').read()
TRUE_SVG = open(os.path.join(BASE_DIR, 'resource/true.svg'), encoding='utf8').read()
FALSE_SVG = open(os.path.join(BASE_DIR, 'resource/false.svg'), encoding='utf8').read()


class Base:
    def __init__(self, data=None, **kwargs):
        if data:
            if isinstance(data, str):
                data = json.loads(data)
            self.load_data(data)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def load_data(self, data):
        # do something by override
        pass


class Doc(Base):
    title = 'API Document'
    version = 'v1.0.0'
    host = 'http://rest.api.com'
    description = ''
    notes = []
    apis = []

    def build(self, target=None, language='en'):
        # language: zh, en ...
        template = open(os.path.join(BASE_DIR, 'resource/template.html'), encoding='utf8').read()
        html = Template(template, strip=False).expand(
            doc=self, markdown=mistune.markdown, style=STYLE, language=language)
        if target:
            open(target, 'w', encoding='utf8').write(html)
        print(f'{self.title} build successful!')
        return html

    def add_note(self, *args, **kwargs):
        note = Note(*args, **kwargs)
        self.notes.append(note)

    def add_api(self, *args, **kwargs):
        api = Api(*args, **kwargs)
        self.apis.append(api)

    def load_data(self, data):
        self.title = data.get('title', self.title)
        self.version = data.get('version', self.version)
        self.host = data.get('host', self.host)
        self.description = data.get('description', self.description)

        notes = data.get('notes')
        apis = data.get('apis')

        if notes:
            self.notes = [Note(d) for d in notes]

        if apis:
            self.apis = [Api(d) for d in apis]

    def to_dict(self):
        return {
            'title': self.title,
            'version': self.version,
            'host': self.host,
            'description': self.description,
            'notes': [n.to_dict() for n in self.notes],
            'apis': [a.to_dict() for a in self.apis],
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class Note(Base):
    title = ''
    content = ''

    def load_data(self, data):
        self.title = data.get('title', self.title)
        self.content = data.get('content', self.content)

    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content,
        }


class Api(Base):
    title = ''
    uri = '/'
    method = 'GET'
    description = ''
    uri_params = []
    query_params = []
    post_params = []
    content_types = ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data']
    body_example = ''
    response_example = ''
    tips = ''

    @property
    def id(self):
        return id(self)

    def load_data(self, data):
        self.title = data.get('title', self.title)
        self.uri = data.get('uri', self.uri)
        self.method = data.get('method', self.method)
        self.description = data.get('description', self.description)
        self.content_types = data.get('content_types', self.content_types)
        self.body_example = data.get('body_example', self.body_example)
        self.response_example = data.get('response_example', self.response_example)
        self.tips = data.get('tips', self.tips)

        uri_params = data.get('uri_params')
        query_params = data.get('query_params')
        post_params = data.get('post_params')

        if uri_params:
            self.uri_params = [UriParam(d) for d in uri_params]

        if query_params:
            self.query_params = [QueryParam(d) for d in query_params]

        if post_params:
            self.post_params = [PostParam(d) for d in post_params]

    def to_dict(self):
        return {
            'title': self.title,
            'uri': self.uri,
            'method': self.method,
            'description': self.description,
            'content_types': self.content_types,
            'body_example': self.body_example,
            'response_example': self.response_example,
            'tips': self.tips,
            'uri_params': [p.to_dict() for p in self.uri_params],
            'query_params': [p.to_dict() for p in self.query_params],
            'post_params': [p.to_dict() for p in self.post_params],
        }


class Param(Base):
    name = ''
    type = 'string'
    description = ''
    required = False
    default = ''
    example = ''

    @property
    def required_svg(self):
        if self.required:
            return TRUE_SVG
        else:
            return FALSE_SVG

    def load_data(self, data):
        self.name = data.get('name', self.name)
        self.type = data.get('type', self.type)
        self.description = data.get('description', self.description)
        self.required = data.get('required', self.required)
        self.default = data.get('default', self.default)
        self.example = data.get('example', self.example)

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'description': self.description,
            'required': self.required,
            'default': self.default,
            'example': self.example,
        }

    
class UriParam(Param):
    required = True


class QueryParam(Param):
    pass


class PostParam(Param):
    pass



UP = UriParam
QP = QueryParam
PP = PostParam

