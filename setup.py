from pathlib import Path
from distutils.core import setup


def get_version():
    basedir = Path(__file__).parent
    with open(basedir / 'urlazy.py') as f:
        version_line = next(line for line in f
                            if line.startswith('__version__'))
        return eval(version_line.split('=')[1])
    raise RuntimeError('No version info found.')


def get_long_description():
    basedir = Path(__file__).parent
    with open(basedir / 'README.txt') as f:
        long_description = f.read()
    return long_description


setup(
    name='URLazy',
    version=get_version(),
    py_modules=['urlazy'],
    author='Iwan Trofimtschuk',
    author_email='iwan@djangsters.de',
    url='https://github.com/i-trofimtschuk/urlazy/',
    license='Unlicense',
    description='URLazy lets you build URLs incrementally with ease',
    long_description=get_long_description(),
    platforms=['any'],
    classifiers=[
        'License :: OSI Approved :: The Unlicense (Unlicense)',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
