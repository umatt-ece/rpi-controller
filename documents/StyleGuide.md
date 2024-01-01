# Style Guide

---

> This document outlines the expected style/format of code in this repository. The purpose for this is to develop consistency and clarity throughout the project. It is the responsibility of any contributors to the project to abide by these standards.

## General

In general, this repository follows the [PEP8](https://peps.python.org/pep-0008/) standard for python code. When in doubt, you can refer to [pep8.org](https://pep8.org/) for questions on how to structure and format your code.

> ### Note about automatic formatting
> With many editors (in particular PyCharm and other JetBrain tools), IDE tools are provided for automatic code formatting. In PyCharm, this can be performed with the keyboard shortcuts `ctrl`+`shift`+`L` (for full file optimization) and `ctrl`+`shift`+`O` (for imports optimization). By default, these tools do a very good job with formatting; however, often times the settings must be tweaked.
> 
> Rather than making everyone perform the same changes to the settings, these settings can be imported from the folder [pycharm-settings.zip](pycharm-settings.zip).

## Line Length
For all Python files, no line should exceed 120 characters in length.

## Naming

**Files** should be named according to the following:
```
Python:   snake_case.py
Shell:    kebab-case.sh
Batch:    kebab-case.bat
Markdown: PascalCase.md
```

Within _Python_ files, the following naming conventions apply:
```
constants: UPPER_CASE
variables: snake_case
functions: snake_case
classes:   PascalCase
```

## File Structure

```python
"""
File Description (optional)
"""
import base_modules      # ex. "logging", "time", etc...

import external_modules  # ex. "redis", "fastapi", etc...

import project_modules   # ex. "DataStore", "MCP23S17", etc...

FILE_CONSTANTS = ""


def file_functions():
    pass


class FileClasses:
    pass

```

> **Note:** An empty line should always be present at the end of a file. This convention is followed for historical reasons, but provides extra safety for certain legacy libraries and operating systems.

## Type Hinting

Unlike many other languages, Python does not enforce static variable types. In other words, any variable can be of any datatype, and can change datatypes at any time. This makes for a lot of flexibility, but also confusion. Like how do you know what type of variable to expect when writing a function? Thankfully, Python has a solution! While we can't _enforce_ variables to be of a certain type, we cane _hint_ at what type they should be.

```python
from typing import Any, Union


def function(integer: int, list_or_dict: Union[list, dict], whatever: Any) -> bool:
    """
    :param integer: First parameter should be an integer.
    :param list_or_dict: Second parameter should be either a list or dictionary.
    :param whatever: Third parameter can be of any type.
    :returns: This function is expected to return a boolean.
    """
    pass
```

## Class Structure

```python
import ParentClass


class ClassName(ParentClass):
    """
    Description of class & relevant information.
    """
    CLASS_CONSTANTS = ""

    _class_variables = None

    def __init__(self, variables: type) -> None:
        super().__init__(variables)  # Call to parent constructor if applicable
        self._class_variables = variables
    
    def public_class_functions(self, var: type) -> None:
        """
        Description of public function.
        
        :param var: details about parameter `var` (units, assumptions, etc...)
        :returns: details about returned value (units, assumptions, etc...)
        """
        pass
        
    def _private_class_functions(self) -> None:
        """
        Description of private function.
        """
        pass
    
    @staticmethod
    def static_functions() -> None:
        """
        For straight-forward and simple functions, a doc-string is not always necessary.
        """
        pass
    
    @property
    def class_variable(self) -> type:
        return self._class_variables
```

> **Note:** In Python, anyone can be anything and everyone can access everything. This is one of the things that makes it such a powerful language; but, "with great power comes great responsibility" (good 'ol uncle Ben). While we can't _enforce_ restrictive scope, we can at least help _hint_ at it.
> 
> All _public_ class variables and functions (those intended to be accessed outside the scope of the class) are named in regular `snake_case` while _private_ class variables and functions (those that should _only_ ever be accessed withing the context of the given class) are named with a leading underscore `_snake_case`.
> 
> If you want to expose a private class variable, you can do so by creating class 'attributes' using the `@property` decorator.
> 
> Ultimately, it's up the next programmer to honour these conversions and not access stuff they shouldn't, but at least you can tell them "told you so" when their code ends up breaking.
