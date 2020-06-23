#coding=utf8

from setuptools import setup, find_packages


try:
    long_description = open('README.md').read()
except Exception as e:
    long_description = ''


install_requires = []
for line in open('requirements.txt').readlines():
    line = line.strip()
    if line and not line.startswith('#'):
        install_requires.append(line)


setup(
    name='eave',
    version='0.1.2',
    description='A Restful Api Document Builder For Pythonista',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='tao.py',
    author_email='taojy123@163.com',
    maintainer='tao.py',
    maintainer_email='taojy123@163.com',
    install_requires=install_requires,
    license='MIT License',
    packages=find_packages(),
    include_package_data=True,
    platforms=["all"],
    url='https://github.com/taojy123/eave',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
)
