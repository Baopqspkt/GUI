from cx_Freeze import setup, Executable

setup(
		name = "Any Name",
		version = "3.1" ,
		description = "Any Description you like",
		executables = [Executable("G4-4.py",base = "Win32GUI")])