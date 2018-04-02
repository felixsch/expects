from setuptools import setup, find_packages

test_requirements = [
    'pytest',
    'expects'
]

setup(
    name='receives',
    version='0.0.1',
    description='A function call assertion library',
    long_description='A library to match function/method calls in tests',
    url='https://github.com/felixsch/receive',
    author='Felix Schnizlein',
    author_email='felix@schnizle.in',
    licence='MIT',
    packages=find_packages(exclude=['spec']),
    test_requires=test_requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Licence :: OSI Approved MIT Licence',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers'
    ]
)
