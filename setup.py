from distutils.core import setup
import py2exe
import sys

sys.argv.append('py2exe')

setup(
    options={'py2exe': {'bundle_files': 1, 'compressed': True}},
    console=[{'script': "pping.py"}],
    zipfile=None,
)
