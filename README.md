# tagterm [![Documentation Status](https://readthedocs.org/projects/tagterm/badge/?version=latest)](http://tagterm.readthedocs.io/?badge=latest)

Remove tags from validated XHTML files.


## Installation

Clone repository, then install Python interpreter:
```bash
git clone https://github.com/cmin764/tagterm.git
cd tagterm

sudo apt update && sudo apt install --upgrade python python-dev python-setuptools
sudo -H easy_install -U pip
```

Install 3rd party libraries and packages:
```bash
sudo apt install --upgrade libtidy-dev
sudo -H pip install -Ur requirements.txt
sudo python setup.py develop
```

Run tests and create documentation:
```bash
nosetests
cd docs
make html
cd ../
```


## Usage

Run CLI and explore API commands:
```bash
tagterm --help

tagterm validate -i res/simple.html
tagterm convert -i res/simple.html
tagterm remove -i res/simple-convert.xhtml

cat res/simple*
```
Then you should see this:
```xml
<?xml version="1.0" ?>
<xml>

Title of the document

	<h1>
Welcome
</h1>


	<p>
Hello World!
</p>


</xml>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>
      Title of the document
    </title>
  </head>
  <body>
    <h1>
      Welcome
    </h1>
    <p>
      Hello World!
    </p>
  </body>
</html>
<!DOCTYPE html>

<html>
    <head>
        <title>Title of the document</title>
    </head>

    <body>
        <h1>Welcome</h1>
        <p>Hello World!</p>
    </body>

</html>
```
Which is the final XML file (with removed tags), obtained from the XHTML
file converted from the first **simple.html** resource example file.
Check *tagterm.log* file for further info, whenever you're using the Python
executable/script or the Java wrapper below.

Install Java and run `./main.sh tagterm ../res/error.html` under the *src*
directory to see it in action from a wrapper perspective.

You'll find the kept tags under the *etc/tagterm/tags* file.
Please read the docs for more info.


----

* Authors:
    + Birsanuc George Cristian <george.birsanuc@info.uaic.ro>
    + Corneliu Tamas <corneliu.tamas@info.uaic.ro>
    + Cosmin Poieana <cosmin.poieana@info.uaic.ro>
    + Iacob Radu Constantin <radu.constantin@info.uaic.ro>
    + Paula Roxana Tanasa <paula.tanasa@info.uaic.ro>
    + Tesu Andrei <andrei.tesu@info.uaic.ro>
* Documentation: http://tagterm.readthedocs.io/
* Source: https://github.com/cmin764/tagterm.git
* License: MIT
