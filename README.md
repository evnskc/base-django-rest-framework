[![Test](https://github.com/evnskc/base-django-rest-framework/actions/workflows/test.yml/badge.svg)](https://github.com/evnskc/base-django-rest-framework/actions/workflows/test.yml)
[![Publish](https://github.com/evnskc/base-django-rest-framework/actions/workflows/publish.yml/badge.svg)](https://github.com/evnskc/base-django-rest-framework/actions/workflows/publish.yml)
[![PyPI](https://img.shields.io/pypi/v/base-django-rest-framework)](https://pypi.org/project/base-django-rest-framework/)

# Base Django Rest Framework Project Setup

## Installation

Using ```pip```

```commandline
pip install base-django-rest-framework
```

Using ```poetry```

```commandline
poetry add base-django-rest-framework
```

## Usage

In your project's settings.py

```python
# ...

INSTALLED_APPS = [
    # ...
    "rest_framework",
    "base_django_rest_framework",
    # ...
]

# ...

# Default base_django_rest_framework configurations
from base_django_rest_framework.conf import *  # NOQA
```