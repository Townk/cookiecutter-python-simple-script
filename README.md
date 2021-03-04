# Python Simple Script Cookiecutter


I created this [Cookiecutter](https://github.com/audreyr/cookiecutter) template, to kickstart my
personal and work related python scripts. I wanted to have all the validations and checks configured
while keeping it simple.

I got a great deal of inspiration from two fantastic Cookiecutters:

- [cookiecutter-hypermodern-python](https://github.com/cjolowicz/cookiecutter-hypermodern-python)
- [Python Packages Project Generator](https://github.com/TezRomacH/python-package-template)

So, why I didn't use these templates instead of creating mine?

Mostly because I wanted to learn a little bit more about Cookiecutter, but also because I'm a bit
nit picker when it comes to project structures.

## Usage

There is a caveat to use my template. You must use Cookiecutter from top of the tree. The reason for
that is a feature I use on the template to define values to variables that the user should not need
to see or complete when the template engine starts.

You can get the Cookiecutter top of the tree with pip:

```shell
$ pip3 install 'git+git://github.com/cookiecutter/cookiecutter.git'
```

Once you have the latest Cookiecutter, you can use my template with the following command:

```shell
$ cookiecutter gh:Townk/cookiecutter-python-simple-script
```

## Features

- Packaging and dependency management with [Poetry][poetry];
- Documentation with Sphinx_ and [Read the Docs][rtd]

[poetry]: https://python-poetry.org/
[rtd]: https://readthedocs.org/
