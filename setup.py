import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"],
                     "excludes": ["tkinter"],
                     "include_files":["img", "object", "param", "fonction"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "DUNE production bobine",
        version = "4.2",
        description = "Analyse production de bobines sur la machine MONDON",
        options = {"build_exe": build_exe_options},
        executables = [Executable(script="main.py",
                                  base=base,
                                  icon="img/logo_dune_production.ico",
                                  targetName="DUNE production bobines.exe")])