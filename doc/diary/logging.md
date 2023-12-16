# Logging

[> Back to TOC](entries.md)

Logging shows up in tests.
When a test fails, the most recent log can help debug where the test failed.

The logging.ini can be split into loggers, handlers, and formatters.
Loggers build the hierarchy based on qualnames.
A qualname 'A.B.C' will also log to 'A.B' and 'A'.

```python
from logging import getLogger
logger = getLogger(__name__)
```

The code block allows logging hierarchy mirrors code modules.
This also allows logs that use `%(name)s` to show where the log was called from.

Handlers write the logs to either stdout or to files.
Log files can grow very large, which slows down writing.
It is best to rotate log files.

Formatters format the log.
`%(asctime)s` is when the message was logged.
It can be customized with `datefmt`.
`%(levelname)s` is the severity of the log.
`%(name)s` is the file that logged the message.
`%(message)s` is the message passed to the logger.
