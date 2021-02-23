package(default_visibility = ["PUBLIC"])

pip_library(
    name = "numpy",
    version = "1.19.5",
    zip_safe = False, # This is because NumPy has shared object files which can't be linked to them when zipped up
)

pip_library(
    name = "matplotlib",
    version = "3.3.4",
        deps = [
        ":numpy",
        ":pyparsing",
        ":cycler",
        ":six",
        ":python-dateutil",
        ":kiwisolver",
        ":pillow",
    ],
)

pip_library(
    name = "pyparsing",
    version = "2.4.7",
)

pip_library(
    name = "cycler",
    version = "0.10.0",
)

pip_library(
    name = "six",
    version = "1.15.0",
)

pip_library(
    name = "python-dateutil",
    version = "2.8.1",
)

pip_library(
    name = "kiwisolver",
    version = "1.3.1",
)

pip_library(
    name = "pillow",
    version = "8.1.0",
)

pip_library(
    name = "PyQt5",
    version = "5.15.2",
    package_name = "PyQt5",
    deps = [
        ":PyQt5-sip",
    ],
    zip_safe = False, # This is because PyQt5 has shared object files which can't be linked to them when zipped up
)

pip_library(
    name = "PyQt5-sip",
    version = "12.8.1",
)
