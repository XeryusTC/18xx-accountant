# -*- coding: utf-8 -*-
import importlib
import unittest
from unipath import Path
import functional_tests

if __name__ == '__main__':
    tests = []
    for test in Path('functional_tests').listdir(pattern='test*.py'):
        name = 'functional_tests.{}'.format(test.stem)
        importlib.import_module(name)
        tests.append(name)

    unittest.main(defaultTest=tests)
