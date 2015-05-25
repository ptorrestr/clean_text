import subprocess
from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

def version():
  out = subprocess.Popen(['git','describe','--tags'], stdout = subprocess.PIPE )
  out.wait()
  if out.returncode:
    with open('version') as f:
      return f.read()
  else:
    m_version = out.stdout.read().strip()
    with open('version', 'w') as f:
      f.write(m_version)
    return m_version

def dependencies():
  with open('dependencies') as f:
    return f.readlines()  

setup(
  name = 'clean_text',
  version = version(),
  description = 'Text cleaner. Remove stopwords and does stemming',
  long_description = readme(),
  classifiers=[
    'Programming Language :: Python :: 3.4',
  ],
  url = 'http://github.com/ptorrest/clean_text',
  author = 'Pablo Torres',
  author_email = 'pablo.torres@deri.org',
  license = 'GNU',
  packages = ['clean_text', 'clean_text.tests'],
  install_requires = dependencies(),
  entry_points = {
    'console_scripts':[
      'clean_text = clean_text.cleaner:main'
    ]
  },
  test_suite = 'clean_text.tests',
  zip_safe = False
)
