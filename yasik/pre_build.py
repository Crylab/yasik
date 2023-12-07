#!/usr/bin/env python
import subprocess
import os

command = "./gradlew" if os.name == "posix" else "gradlew.bat"
subprocess.run([command, "generateGrammarSource"])
