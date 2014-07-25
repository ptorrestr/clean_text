Text cleaner
============

Remove stopwords and perform stemming

Installation
------------
OpenBLAS:
 It is pretty easy to build an own optimized version of openBLAS. First you need get the code and compile it as usually. Then setup the environment and indicate to distribute to build numpy with the openblas library. See here for more info: http://osdf.github.io/blog/numpyscipy-with-openblas-for-ubuntu-1204-second-try.html

Lapack:
Because clean_text is based on nltk, you need install blas and lapack libraries. It is recommeded to install an optimized version of both. This libraries can be found on the package management tools of the linux distribution. (debian: liblapack-dev). 
If you think is worthy, you can build your own optimized version of the library. This tutorial explain exacltly the necessary steps to do so. http://theoryno3.blogspot.ie/2010/12/compiling-lapack-as-shared-library-in.html

It is recomendable to use virtualenv to avoid package conflicts
* virtualenv /SOME/PATH -p python2
* source /SOME/PATH/bin/activate

Automatically install:
* `pip install --index-url http://10.2.16.32/simple clean_text`

Manually install:
* `git clone CLEAN_TEXT_URL`
* `cd clean_text; python setup install`

Numpy over Openblas
* go to the virtualenv folder
* add `source /opt/env/c++/openblas_default` to the bin/activate file
* source /virtualenv/folder/bin/activate
* `mkdir download`
* `mkdir build`
* `pip install -d download numpy`
* `tar -xvf download/numpy*.tar.gz`
* mv download/numpy* build/
* create file build/numpy*/site.cfg. Add the following data:
`
[default]
library_dirs = /opt/usr/local/openblas/lib

[openblas]
libraries = openblas
library_dirs = /opt/usr/local/openblas/lib
include_dirs = /opt/usr/local/openblas/include

[atlas]
atlas_libs = openblas
library_dirs = /opt/usr/local/openblas/lib

[lapack]
lapack_libs = openblas
library_dirs = /opt/usr/local/openblas/lib
`
* python setup.py build/install

Dependencies:
* nltk
* numpy
* t2db\_objects
* sphinx
* pyyaml

Configuration
-------------
You need to install NLTK data.
`python -m nltk.downloader all`

To configure this project, pleae see the configuration example file (etc/example.config)

Execution
---------
Just do
`clean_text -c CONFIG_FILE -o OUTPUT_FILE INPUTFILE` 

Where:
* CONFIG\_FILE The path to the configure file
* OUTPUT\_FILE The path to the output file (if it doesn't exist, it will be created)
* INPUT\_FILE The path to the input file

Documentation
-------------
`cd docs; make html`
