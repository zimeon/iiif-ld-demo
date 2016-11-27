# Setup instructions for iiif-ld-demo

## 1. Check your python

Examples have been tested with Python 2.7, 3.3, 3.4 and 3.5. They will not work with Pythons earlier than 2.7. You can check your version with:

``` bash
> python --version
Python 3.5.1 :: Continuum Analytics, Inc.
```

(I find that a user-space version of Python installed with [miniconda](http://conda.pydata.org/docs/install/quick.html) is very convenient and avoids confusion with the system Python on Macs.)

## 2. Clone the repository

Download a copy by cloning the git repository. The following should create a copy in `iiif-ld-demo` under your current directory:

``` bash
> git clone git@github.com:zimeon/iiif-ld-demo.git
```

(If you want to fix bugs and send them back as pull requests, the best way to do that is to first fork the repository into your own github account and then close that.)

## 3. Change directory into the new copy

``` bash
> cd iiif-ld-demo
```

## 4. Install any missing dependencies

Dependencies are specified in the setuptools file, `setup.py`, and can be installed with:

``` bash
> python setup.py develop
```

## 5. Run the tests

There are some simple tests which check the output of various sample programs against that copied into the markdown files. You can run these with:

``` bash
> python setup.py test
```

(These are the same tests as run by Travis CI to shown the [![Build Status](https://travis-ci.org/zimeon/iiif-ld-demo.svg?branch=master)](https://travis-ci.org/zimeon/iiif-ld-demo) icon on the front page.)

If the tests all pass then you should be good-to-go, otherwise some investigation is needed...
