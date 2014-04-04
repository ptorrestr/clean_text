Text cleaner
============

Remove stopwords and perform stemming

Installation
------------

It is recomendable to use virtualenv to avoid package conflicts
* virtualenv /SOME/PATH -p python2
* source /SOME/PATH/bin/activate

Automatically install:
* `pip install --index-url http://10.2.16.32/simple clean_text`

Manually install:
* `git clone CLEAN_TEXT_URL`
* `cd clean_text; python setup install`

Dependencies:
* nltk
* numpy
* t2db\_objects

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
