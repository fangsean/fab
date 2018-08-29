import sys
from setuptools import setup,find_packages

with open('README.md',encoding='utf-8') as description:
    long_description = description.read()

fabric_package = sys.version_info < (3, 0) and 'Fabric>=1.1,<2.0' or 'Fabric3>=1.1,<2.0'
install_requires = [
    fabric_package,
    'Click',
]
setup(
    name='nq',
    version='1.0',
    author_email='jsen.yin@gmail.com',
    # packages=find_packages('release'),
    py_modules=['nq'],
    description='自定义发布工具',
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        nq=nq:main
    '''
)
