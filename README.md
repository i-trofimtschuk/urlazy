URLazy
------

[![Build Status](https://app.travis-ci.com/i-trofimtschuk/urlazy.svg?branch=master)](https://app.travis-ci.com/i-trofimtschuk/urlazy)

URLazy lets you build or extend existing urls incrementally (lazy) which is it's sole purpose.
To build/extend from existing URLs `from_string` method can be used.

Here are some examples how you can build URLs using URLazy:

	>>> from urlazy import URL, HTTPS

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

	>>> (URL.https().hostname('www.youtube.com').path('watch').query({'v': 'dQw4w9WgXcQ'})).url
	'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

	>>> (HTTPS() // URL().hostname('www.youtube.com') / URL().path('watch') & URL().query({'v': 'dQw4w9WgXcQ'}) | URL().fragment('fragment')).url
	'https://www.youtube.com/watch?v=dQw4w9WgXcQ#fragment'

	>>> (HTTPS() // 'www.youtube.com' / 'path1' / 'path2' / '' & [('a', 1), ('b', 2)] & [('a', 3)] | 'fragment' | '-more-fragment').url
	'https://www.youtube.com/path1/path2/?a=1&b=2&a=3#fragment-more-fragment'

	>>> (URL.https().username('user').password('pwd').hostname('www.youtube.com').port(443).path('/').query([('a', 1), ('b', 2)]).query([('a', 3)]).fragment('fragment').fragment('-more-fragment')).url
	'https://user:pwd@www.youtube.com:443/?a=1&b=2&a=3#fragment-more-fragment'

# extending existing urls
        
	>>> (URL.from_string('https://www.youtube.com/old_path') / 'watch' & 'v=dQw4w9WgXcQ' | 'fragment').url
        'https://www.youtube.com/old_path/watch?v=dQw4w9WgXcQ#fragment'
