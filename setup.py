# This Python file uses the following encoding: utf-8
from setuptools import setup, find_packages

setup(
    name='syncFiles',
    packages=find_packages(),
    version='0.0.2',
    description='Simple file synce.',
    long_description='A simple file syncer, that works with network folders, and checks sums. Windows only.',
    author='Mateusz Krzysztof Łącki',
    author_email='matteo.lacki@gmail.com',
    url='https://github.com/MatteoLacki/syncFiles',
    keywords=[  'simple sys admin tools'],
    classifiers=[   'Development Status :: 1 - Planning',
                    'License :: OSI Approved :: BSD License',
                    'Intended Audience :: Science/Research',
                    'Topic :: Scientific/Engineering :: Chemistry',
                    'Programming Language :: Python :: 3.6',
                    'Programming Language :: Python :: 3.7',
                    'Programming Language :: Python :: 3.8'],
    license="GPL-3.0-or-later",
    install_requires=["flask"],
    scripts = ["bin/syncyWincy.py",
               "bin/checkSummer.py"]
)
