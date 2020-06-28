# NI Host Integration Agent API for FL Studio
Abstraction layer of the Native Instruments' Host Integration Agent API for the FL Studio MIDI Scripting API.

If you are using a Git repository, you can add the layer as a submodule:
```bash
# Adds nihia as a submodule inside your git repository under the folder "nihia"
git submodule add https://github.com/hobyst/flmidi-nihia.git nihia
```

Then, inside your script import it using
```python
from nihia import nihia
```

Used DrivenByMoss by Jürgen Moßgraber as a reference:
https://github.com/git-moss/DrivenByMoss
