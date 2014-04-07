#!/usr/bin/env python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

setup(name='django-toolhub',
      version='0.0.1',
      description='',
      author='Patrick Forringer',
      author_email='patrick@forringer.com',
      #url='',
      #license='',
      packages=[
          'toolhub', 'toolhub.migrations'],
      install_requires=[
          'South',
          'Django>=1.6',],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: End Users/Desktop',
          'Programming Language :: Python',],
     )
