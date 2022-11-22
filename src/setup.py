# -*- coding: utf-8 -*-
#

"""
@Project: easyops
@File:    setup
@Author:  boli
@Data:    2022/11/22 10:44
@Describe: 
    setup
"""

import sys

from setuptools import find_packages, setup

kwargs = {}
if sys.version_info.major > 2:
    kwargs.update({
        "encoding": "utf-8"
    })
with open("README.rst", "r", **kwargs) as f:
    long_description = f.read()

setup(
    name='easyops',
    version='1.0.4',
    author="boli",
    author_email="boli@easyops.cn",
    license="MIT License",
    url="https://www.uwintech.cn/",
    description="uwintech easyops sdk",
    packages=find_packages(),
    long_description=long_description,
    platforms=["all"],
    # All data files are packaged
    package_data={"": ["*"]},
    # Automatically contains version-controlled (svn/git) data files
    include_package_data=True,
    zip_safe=False,
    # Setting dependency Packages
    install_requires=[
        'PyYAML>=5.4.1',
        'requests>=2.27.1'
    ],
)
