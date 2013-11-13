from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='clean_text',
    version='0.0.5',
    description='Text cleaner. Remove stopwords and perform stemming',
    long_description = readme(),
    classifiers=[
      'Programming Language :: Python :: 2.7',
    ],
    url='http://github.com/ptorrest/clean_text',
    author='Pablo Torres',
    author_email='pablo.torres@deri.org',
    license='GNU',
    packages=['clean_text', 'clean_text.tests'],
    install_requires=[
        'nltk >= 2.0.4',
    ],
    entry_points = {
        'console_scripts':[
            'clean_text = clean_text.cleaner:main'
        ]
    },
    test_suite='clean_text.tests',
    zip_safe = False
)
