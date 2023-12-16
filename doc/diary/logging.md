# Logging

[> Back to TOC](entries.md)

Logging doesn't help write code, but it is useful when using it and something goes wrong.
I spent a while working out the kinks.
I made it way more complicated than it needed to be.

```python
from logging import getLogger
logger = getLogger(__name__)
```

This allows logs that use formats that contain `%(name)s` to files to debug.
This is dependent on the `qualname` establishing the log file hierarchy.
