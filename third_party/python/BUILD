package(default_visibility = ["PUBLIC"])

pip_library(
    name = "numpy",
    version = "1.19.5",
    zip_safe = False, # This is because NumPy has shared object files which can't be linked to them when zipped up
)

pip_library(
    name = "matplotlib_isolated",
    package_name = "matplotlib",
    version = "3.3.4",
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

python_library(
    name = "matplotlib",
    srcs = [],
    deps = [
        "//third_party/python:matplotlib_isolated",
        "//third_party/python:pyparsing",
        "//third_party/python:cycler",
        "//third_party/python:six",
        "//third_party/python:python-dateutil",
        "//third_party/python:kiwisolver",
        "//third_party/python:pillow",
    ],
)