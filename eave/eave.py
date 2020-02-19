# python3

import os
import json
import cgi

import mistune
import yaml

from step import Template


__all__ = ['Doc', 'Note', 'Api', 'Param', 'UriParam', 'QueryParam', 'BodyParam', 'UP', 'QP', 'BP', 'readf']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TRUE_SVG = open(os.path.join(BASE_DIR, 'resource/true.svg'), encoding='utf8').read()
FALSE_SVG = open(os.path.join(BASE_DIR, 'resource/false.svg'), encoding='utf8').read()

RESOURCE = {
    'style': open(os.path.join(BASE_DIR, 'resource/style.css'), encoding='utf8').read(),
    'highlight_css': open(os.path.join(BASE_DIR, 'resource/highlight/styles/github.css'), encoding='utf8').read(),
    'highlight_js': open(os.path.join(BASE_DIR, 'resource/highlight/highlight.pack.js'), encoding='utf8').read(),
}


class Base:
    def __init__(self, data=None, **kwargs):
        try:
            data = json.loads(data)
        except:
            pass
        try:
            data = yaml.safe_load(data)
        except:
            pass
        if data:
            self.load_data(data)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def load_data(self, data):
        # do something by override
        pass

    def to_dict(self):
        # do something by override
        return {}

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    def to_yaml(self):
        return yaml.safe_dump(self.to_dict())

    def clone(self):
        data = self.to_dict()
        return self.__class__(data)


class Doc(Base):
    title = 'API Document'
    version = 'v1.0.0'
    host = 'http://rest.api.com'
    description = ''
    notes = None
    apis = None
    ending = ''
    template = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notes = self.notes or []
        self.apis = self.apis or []

    def build(self, target=None, language='en'):
        # language: zh / en ...
        if not self.template:
            self.template = os.path.join(BASE_DIR, 'template.html')
        template = open(self.template, encoding='utf8').read()
        html = Template(template, strip=False).expand(
            doc=self, markdown=mistune.markdown, resource=RESOURCE, language=language)
        if target:
            open(target, 'w', encoding='utf8').write(html)
        print(f'{self.title} build successful!')
        return html

    def add_note(self, *args, **kwargs):
        note = Note(*args, **kwargs)
        self.notes.append(note)
        return note

    def add_api(self, *args, **kwargs):
        api = Api(*args, **kwargs)
        self.apis.append(api)
        return api

    def load_data(self, data):
        self.title = data.get('title', self.title)
        self.version = data.get('version', self.version)
        self.host = data.get('host', self.host)
        self.description = data.get('description', self.description)
        self.ending = data.get('ending', self.ending)

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
            'ending': self.ending,
        }


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
    uri = ''
    method = 'GET'
    description = ''
    uri_params = None
    query_params = None
    body_params = None
    content_types = ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data']
    body_example = ''
    response_description = ''
    response_example = ''
    tips = ''
    from_md = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uri_params = self.uri_params or []
        self.query_params = self.query_params or []
        self.body_params = self.body_params or []
        if self.from_md:
            self.from_md = readf(self.from_md)
        
    @property
    def id(self):
        return id(self)
        
    @property
    def uri_escape(self):
        return cgi.escape(self.uri)

    def load_data(self, data):
        self.title = data.get('title', self.title)
        self.uri = data.get('uri', self.uri)
        self.method = data.get('method', self.method)
        self.description = data.get('description', self.description)
        self.content_types = data.get('content_types', self.content_types)
        self.body_example = data.get('body_example', self.body_example).strip()
        self.response_description = data.get('response_description', self.response_description).strip()
        self.response_example = data.get('response_example', self.response_example).strip()
        self.tips = data.get('tips', self.tips)
        self.from_md = data.get('from_md', self.from_md)

        uri_params = data.get('uri_params')
        query_params = data.get('query_params')
        body_params = data.get('body_params')

        if uri_params:
            self.uri_params = [UriParam(d) for d in uri_params]

        if query_params:
            self.query_params = [QueryParam(d) for d in query_params]

        if body_params:
            self.body_params = [BodyParam(d) for d in body_params]

    def to_dict(self):
        return {
            'title': self.title,
            'uri': self.uri,
            'method': self.method,
            'description': self.description,
            'content_types': self.content_types,
            'body_example': self.body_example,
            'response_description': self.response_description,
            'response_example': self.response_example,
            'tips': self.tips,
            'from_md': self.from_md,
            'uri_params': [p.to_dict() for p in self.uri_params],
            'query_params': [p.to_dict() for p in self.query_params],
            'body_params': [p.to_dict() for p in self.body_params],
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
            # return FALSE_SVG
            return ''

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


class BodyParam(Param):
    pass


UP = UriParam
QP = QueryParam
BP = BodyParam


def readf(path, encoding='utf8'):
    if os.path.exists(path):
        return open(path, encoding=encoding).read()
    print(f'WARNING: {path} is not found!')
    return ''
