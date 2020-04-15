#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='dbunit',
    version=0.2,
    description=(
        'Python写的一个仿Java DbUnit的数据库单元测试工具'
    ),
    long_description='dbunit',
    long_description_content_type="text/markdown",
    author='Wang Junjie',
    author_email='shwangjj@163.com',
    maintainer='Wang Junjie',
    maintainer_email='shwanjj@163.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/shwdbd/dbunit',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.7",
    # 需要安装的依赖
    install_requires=[
        'mysql-connector-python==8.0.19',
    ],
)