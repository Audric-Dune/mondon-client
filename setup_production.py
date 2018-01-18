import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"],
                     "excludes": ["tkinter"],
                     "include_files": ["assets", "constants", "lib", "stores", "ui", "models"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="DUNE production bobine 3.0",
      version="3.0",
      description="Analyse production de bobines sur la machine Mondon",
      options={"build_exe": build_exe_options},
      executables=[Executable(script="main_production.py",
                              base=base,
                              icon="commun/assets/icons/logo_dune_production.ico",
                              targetName="DUNE_production_bobines.exe")])
