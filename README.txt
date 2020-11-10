URLazy
------

URLazy lets you build urls incrementally (lazy) which is it's sole purpose.
Parsing or modifying URLs is explicitly out ouf scope of this project.

Here are some examples how you can build URLs using URLazy:

>>> from urlazy import URL, HTTPS

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

