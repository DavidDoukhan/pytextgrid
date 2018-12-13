#!/usr/bin/env python
# encoding: utf-8

# The MIT License

# Copyright (c) 2018 David Doukhan - david.doukhan@gmail.com

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import os
from setuptools import setup, find_packages


KEYWORDS = '''
praat
textgrid
python
phonetics'''.strip().split('\n')

CLASSIFIERS=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Multimedia :: Sound/Audio',
    'Topic :: Multimedia :: Sound/Audio :: Analysis',
    'Topic :: Multimedia :: Sound/Audio :: Speech',
    'Topic :: Scientific/Engineering',
    'Topic :: Utilities',
]

DESCRIPTION='A toolbox for manipulating praat textgrid in python: creation, modification, analysis'
#LONGDESCRIPTION=

setup(
    name = "pytextgrid",
    version = "0.1",
    author = "David Doukhan",
    author_email = "david.doukhan@gmail.com",
    description = DESCRIPTION,
    license = "MIT",
    #install_requires=['numpy', 'keras', 'scikit-image', 'sidekit', 'pyannote.algorithms'],
 #   keywords = "example documentation tutorial",
    url = "https://github.com/DavidDoukhan/pytextgrid",
#    packages=['inaSpeechSegmenter'],
    keywords = KEYWORDS,
    packages = find_packages(),
    #package_data = {'inaSpeechSegmenter': ['*.hdf5']},
    #include_package_data = True,
    data_files = ['LICENSE'],
#    long_description=LONGDESCRIPTION,
#    long_description_content_type='text/markdown',
    #scripts=[os.path.join('scripts', script) for script in \
    #         ['ina_speech_segmenter.py']],
    classifiers=CLASSIFIERS,
    #python_requires='>=3',
)
