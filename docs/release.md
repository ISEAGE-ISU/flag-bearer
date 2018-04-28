Release Process
===============
1. Bump the version number in `flag_bearer/__init__.py`.
2. Tag the release in git
3. Install and setup [twine][twine]
4. Generate the source distribution and wheel
    ```bash
    $ python setup.py sdist bdist_whell
    ```

5. (optional) Upload to Test PyPI to verify things are correct.
    ```bash
    $ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    username: ...
    password: ...
    ```

6. Upload to [PyPi][pypi]
    ```bash
    $ twine upload dist/*
    ```

[twine]: https://github.com/pypa/twine
[pypi]: https://pypi.org/p/flag-bearer
