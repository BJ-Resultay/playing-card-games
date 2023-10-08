[//]: # (documentation for full project)

# Playing Card Games

Python programming on various playing card games

Card games are fun and I love python.
This project is to help me learn good coding practices.
It will (hopefully) include various games.

## Games

- [ ] blackjack

## Notes

Python version used is 3.11.2.
Python minimum version is 3.9, which supports type hints.
Shell used is bash.

## Things I learned

The reason I started this project is to learn good coding practices.
It would be simply useless to forget them after finishing this project.
Therefore, I'm documenting them in the most likely place for me to find them again.
This section contains no instructions.
Feel free to ignore this section.

### Github

Considering this repository is on Github, this should not need introduction.
I've used Github in a couple of projects before for several college projects, but it was never the focus.
The only knobs I've turned are branch protection rules and workflows.
The former protects my code from someone trying to nuke it.
The latter automates testing and ensures my build is clean.

### Logging

Logging doesn't help write code, but it is useful when using it and something goes horribly wrong.
I definitely spent awhile working out the kinks.
I made it way more complicated than it really needed to be.

```python
from logging import getLogger
logger = getLogger(__name__)
```

This allows logs that use formats that contain `%(name)s` to files to debug.
This is dependent on the `qualname` establishing the log file hierarchy.

### Makefile

Makefiles are the crutch to abstract complicated terminal commands into a simple target.
It's the first thing that was setup, including virtual environments.
I didn't use them since freshmen year because they were very intimidating.
There wasn't much difference between running `python3 file.py` vs `make run` to me.
This was until I was in a situation where the project I was in did not have a Makefile and not using any languages I knew.
Not having a common language severely hampered my ability to write code.
When testing, I cannot even imagine a world where I have to type `./venv/bin/pytest tests` instead of `make test`.

### Python

After learning C/C++ in freshmen year, I fell in love with python so I didn't have to use closing braces.
I can relate to the PEP 20 - The Zen of Python.
I obviously like writing beautiful code.
It's a major reason why I used a linter and an IDE when writing code.
It's also why I continuously refactor my code all the time.
If anyone is depending on my code, I apologize sincerely.

### Testing

Automated testing is a staple of quality assurance.
Clean tests inspire confidence in my code.
Unit tests are fast.
Mocks are magic.
Pytest discovery in VS Code was a bitch.
FYI, `__init__.py` needs to be added to the entire branch so pytest can find the source code.

### VS Code

I used to exclusively use terminal and vim during college.
It worked great with single files.
As I worked with more files, I needed more windows.
Now, I have a million bits and bobs that help me code or make me scramble for documentation.

### VS Code Extensions

This setup allows me to fix bad coding practices while writing code.

- autoDocstring - Python Docstring Generator

    This standardizes my documentation.

- markdownlint

    This lints markdown files, obviously.

- Pylance

    This tells me if the code does not work.

- Pylint

    This standardizes my coding and points out my habits.

- Python

    This lets me code in Python on VS Code.

- Python Indent

    This automatically sets my cursor at the correct indentation.
    Though I am not keen on hanging indents very much.

- Todo Tree

    This keeps tabs on various notes in the code.
