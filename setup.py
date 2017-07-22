from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='gherkin-locust',
    version='0.1',
    description='Locust + Gherkin + Fixture generator',
    long_description=readme(),
    classifiers=[
        'Development Status :: 0.1 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Testing',
    ],
    url='https://github.com/sergeyglazyrindev/gherkin-locust',
    author='Sergey Glazyrin',
    author_email='sergey.glazyrin.dev@gmail.com',
    license='MIT',
    packages=['gherkin_locust', ],
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
    install_requires=[
        'easytest>=0.0.1', 'gherkin-official>=4.1.3',
        'locustio==0.7.5', 'SQLAlchemy==1.1.11'
    ],
    dependency_links=[
        'git+https://bitbucket.org/sergeyglazyrindev/python-easytest.git#egg=easytest-1.0.0',
        'git+https://github.com/cucumber/cucumber/tree/master/gherkin.git#egg=gherkin-official-4.1.3&subdirectory=python'
    ],
    extras_require={
        'dev': [
            'coverage',
            'nose',
            'pytest',
            'pytest-pep8',
            'pytest-cov',
            'mock'
        ],
    },
)
