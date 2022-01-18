from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple, Union
from urllib.parse import ParseResult, parse_qsl, urlencode, urlparse

__version__ = '0.0.1.dev'

Query = List[Tuple[str, str]]
Path = List[str]


@dataclass()
class URL:
    """Build URLs incrementally

    # syntactic sugar
    >>> str(HTTPS() // 'www.youtube.com' / 'watch' & 'v=dQw4w9WgXcQ' | 'fragment')
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ#fragment'

    # one way
    >>> url = HTTPS() // 'www.youtube.com'

    >>> video_id = 'dQw4w9WgXcQ'

    >>> tracking = {'utm_campaign': 'utmc', 'utm_source': 'utms', 'utm_medium': 'utmm'}

    >>> if video_id:
    ...     url /= 'watch'
    ...     url &= {'v': video_id}

    >>> if tracking:
    ...     url &= tracking

    >>> url.geturl()
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ&utm_campaign=utmc&utm_source=utms&utm_medium=utmm'

    # another way
    >>> url = URL().https()

    >>> url.hostname('www.youtube.com')
    URL(_scheme='https', _username='', _password='', _hostname='www.youtube.com', _port='', _path=[], _query=[], _fragment='')

    >>> video_id = 'dQw4w9WgXcQ'

    >>> tracking = {'utm_campaign': 'utmc', 'utm_source': 'utms', 'utm_medium': 'utmm'}

    >>> if video_id:
    ...     url.path('watch')
    ...     url.query({'v': video_id})
    URL(_scheme='https', _username='', _password='', _hostname='www.youtube.com', _port='', _path=['watch'], _query=[], _fragment='')
    URL(_scheme='https', _username='', _password='', _hostname='www.youtube.com', _port='', _path=['watch'], _query=[('v', 'dQw4w9WgXcQ')], _fragment='')

    >>> if tracking:
    ...     url.query(tracking)
    URL(_scheme='https', _username='', _password='', _hostname='www.youtube.com', _port='', _path=['watch'], _query=[('v', 'dQw4w9WgXcQ'), ('utm_campaign', 'utmc'), ('utm_source', 'utms'), ('utm_medium', 'utmm')], _fragment='')

    >>> url.geturl()
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ&utm_campaign=utmc&utm_source=utms&utm_medium=utmm'

    # other examples
    >>> (HTTPS() // 'www.youtube.com' / 'watch' & {'v': 'dQw4w9WgXcQ'}).url
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

    >>> URL.https().hostname('www.youtube.com').path('watch').query({'v': 'dQw4w9WgXcQ'}).url
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

    >>> (HTTPS() // URL().hostname('www.youtube.com') / URL().path('watch') & URL().query({'v': 'dQw4w9WgXcQ'}) | URL().fragment('fragment')).url
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ#fragment'

    >>> (HTTPS() // 'www.youtube.com' / 'path1' / 'path2' / '' & [('a', 1), ('b', 2)] & [('a', 3)] | 'fragment' | '-more-fragment').url
    'https://www.youtube.com/path1/path2/?a=1&b=2&a=3#fragment-more-fragment'

    >>> URL.https().username('user').password('pwd').hostname('www.youtube.com').port(443).path('/').query([('a', 1), ('b', 2)]).query([('a', 3)]).fragment('fragment').fragment('-more-fragment').url
    'https://user:pwd@www.youtube.com:443/?a=1&b=2&a=3#fragment-more-fragment'

    >>> URL.from_string('https://user:pwd@www.youtube.com:443/?a=1&b=2&a=3#fragment-more-fragment').url
    'https://user:pwd@www.youtube.com:443/?a=1&b=2&a=3#fragment-more-fragment'

    >>> (URL.from_string('https://user:pwd@www.youtube.com:443/?a=1&b=2&a=3#fragment-more-fragment') & {'tracking': 'param'}).url
    'https://user:pwd@www.youtube.com:443/?a=1&b=2&a=3&tracking=param#fragment-more-fragment'

    >>> (URL.from_string('https://www.youtube.com') / 'watch' & 'v=dQw4w9WgXcQ' | 'fragment').url
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ#fragment'
    """
    _scheme: str = ''
    _username: str = ''
    _password: str = ''
    _hostname: str = ''
    _port: str = ''
    _path: Path = field(default_factory=list)
    _query: Query = field(default_factory=list)
    _fragment: str = ''

    @staticmethod
    def http() -> URL:
        return URL().scheme('http')

    @staticmethod
    def https() -> URL:
        return URL().scheme('https')

    def scheme(self, scheme: str) -> URL:
        self._scheme = scheme
        return self

    def username(self, username: str) -> URL:
        self._username = username
        return self

    def password(self, password: str) -> URL:
        self._password = password
        return self

    def hostname(self, hostname: str) -> URL:
        self._hostname = hostname
        return self

    def port(self, port: Union[int, str]) -> URL:
        self._port = str(port)
        return self

    @property
    def _netloc(self) -> str:
        netloc = ''
        if self._username:
            if self._password:
                netloc += f'{self._username}:{self._password}@'
            else:
                netloc += f'{self._username}@'
        netloc += self._hostname
        if self._port:
            netloc += f':{self._port}'
        return netloc

    def path(self, path: str) -> URL:
        self._path.append(path)
        return self

    def query(self, query: Union[Query, dict, str]) -> URL:
        if isinstance(query, str):
            self._query.extend(parse_qsl(query))
        elif isinstance(query, dict):
            self._query.extend(query.items())
        else:
            self._query.extend(query)
        return self

    def fragment(self, fragment: str) -> URL:
        self._fragment += fragment
        return self

    def geturl(self) -> str:
        return self.parse_result.geturl()

    def __str__(self):
        return self.geturl()

    @property
    def url(self) -> str:
        return self.geturl()

    @property
    def parse_result(self) -> ParseResult:
        return ParseResult(
            scheme=self._scheme,
            netloc=self._netloc,
            path='/'.join(self._path),
            params='',
            query=urlencode(self._query),
            fragment=self._fragment)

    @staticmethod
    def from_string(url: str) -> URL:
        parse_result = urlparse(url)
        url_obj = URL().scheme(parse_result.scheme)

        auth, _, host_port = parse_result.netloc.rpartition('@')
        if auth:
            _username, _, _password = auth.partition(':')
            url_obj.username(_username)
            if _password:
                url_obj.password(_password)
        _hostname, _, _port = host_port.partition(':')
        url_obj.hostname(_hostname)
        if _port:
            url_obj.port(_port)

        url_obj._path = parse_result.path.split('/')
        url_obj._query = parse_qsl(parse_result.query)
        url_obj._fragment = parse_result.fragment

        return url_obj

    def __floordiv__(self, other: Union[URL, str]) -> URL:
        if isinstance(other, URL):
            self._username = other._username
            self._password = other._password
            self._hostname = other._hostname
            self._port = other._port
        else:
            if '@' in other:
                auth, _, host_port = other.partition('@')
                if ':' in auth:
                    self._username, self._password = auth.split(':', 1)
                else:
                    self._username, self._password = auth, ''
            else:
                host_port = other

            if ':' in host_port:
                self._hostname, self._port = host_port.split(':', 1)
            else:
                self._hostname, self._port = host_port, ''
        return self

    def __truediv__(self, other: Union[URL, str]) -> URL:
        if isinstance(other, URL):
            self._path.extend(other._path)
            return self
        return self.path(other)

    def __and__(self, other: Union[URL, dict]) -> URL:
        if isinstance(other, URL):
            self._query.extend(other._query)
            return self
        return self.query(other)

    def __or__(self, other: Union[URL, str]) -> URL:
        if isinstance(other, URL):
            return self.fragment(other._fragment)
        return self.fragment(other)


HTTP = URL.http
HTTPS = URL.https

if __name__ == "__main__":
    import doctest
    doctest.testmod()
