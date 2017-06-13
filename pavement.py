# -*- coding: utf-8 -*-

import os
import sys

from paver.easy import task, consume_args, needs


@task
def django_setup(pavement_file):
    sys.path.append(os.path.dirname(pavement_file))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'chloroform.tests.settings'
    from django import setup
    setup()


@task
@consume_args
@needs('django_setup')
def django(args):
    from django.core.management import call_command
    call_command(*args)


@task
@needs('django_setup')
def po():
    ignore_list = [
        'setup.py',
        'pavement.py',
        'build/*',
        'requirements.txt',
        'docs/*',
        'requirements.d/*',
    ]
    command = ['makemessages', '-l', 'fr']
    for i in ignore_list:
        command.extend(['-i', i])
    from django.core.management import call_command
    call_command(*command)


def find_version(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'r') as init:
        for line in init:
            if line.startswith('__version__'):
                x, version = line.split('=', 1)
                return version.strip().strip('\'"')
        else:
            raise ValueError('Cannot find the version in {0}'.format(filename))


def parse_requirements(requirements_txt):
    requirements = []
    try:
        with open(requirements_txt, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                if line.startswith('-'):
                    raise ValueError('Unexpected command {0} in {1}'.format(
                        line,
                        requirements_txt,
                    ))

                requirements.append(line)
        return requirements
    except IOError:
        return []


@task
def setup_options():
    import setuptools
    from paver.setuputils import setup
    readme_md = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_md, 'r') as readme_file:
        readme = readme_file.read()

    setup(
        name='chloroform',
        version=find_version('chloroform/__init__.py'),
        description='Contact form Builder',
        long_description=readme,
        author='Grégoire ROCHER',
        author_email='gregoire@emencia.com',
        packages=setuptools.find_packages(
            exclude=[
                '*.tests',
                '*.tests.*',
            ]
        ),
        include_package_data=True,
        install_requires=parse_requirements('requirements.txt'),
        zip_safe=False,
    )


if os.path.realpath(sys.argv[0]) == os.path.realpath(os.path.join(os.path.dirname(__file__), 'setup.py')):
    setup_options()
