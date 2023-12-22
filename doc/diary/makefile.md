# Makefile

[> Back to TOC](entries.md)

Makefiles abstract complicated terminal commands into a simple target.
It is the first thing that was set up, including virtual environments.
It handles dependencies that have been changed.
When testing, it is more concise to type `make test` rather than `venv/bin/pytest tests`.
`.PHONY` targets will always build even when a file of the same name has not been touched.
The target 'help' uses double pound symbols to notate documentation.
My most common targets are 'test', 'lint', and 'coverage'.
That is because these targets ensure my code is high quality.
Running them quickly increases productivity.
