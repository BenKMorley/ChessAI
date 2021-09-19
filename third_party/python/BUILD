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


pip_library(
    name = "absl-py",
    version = "0.13.0",
    deps = [
        ":six",
    ],
)


pip_library(
    name = "astunparse",
    version = "1.6.3",
    deps = [
        ":six",
        ":wheel",
    ],
)

pip_library(
    name = "wheel",
    version = "0.37.0",
)

pip_library(
    name = "clang",
    version = "5.0",
)

pip_library(
    name = "flatbuffers",
    version = "1.12",
)

pip_library(
    name = "gast",
    version = "0.4.0",
)

pip_library(
    name = "google-pasta",
    version = "0.2.0",
    deps = [
        ":six",
    ],
)

pip_library(
    name = "grpcio",
    version = "1.40.0",
    deps = [
        ":six",
    ],
)

pip_library(
    name = "h5py",
    version = "3.1.0",
    deps = [
        ":numpy",
    ],
)

pip_library(
    name = "keras",
    version = "2.6.0",
)

pip_library(
    name = "Keras-Preprocessing",
    version = "1.1.2",
    deps = [
        ":numpy",
        ":six",
    ],
)

pip_library(
    name = "opt-einsum",
    version = "3.3.0",
    deps = [
        ":numpy",
    ],
)

pip_library(
    name = "protobuf",
    version = "3.18.0",
)

pip_library(
    name = "cachetools",
    version = "4.2.2",
)

pip_library(
    name = "pyasn1",
    version = "0.4.8",
)

pip_library(
    name = "pyasn1-modules",
    version = "0.2.8",
    deps = [
        ":pyasn1",
    ],
)

pip_library(
    name = "rsa",
    version = "4.7.2",
    deps = [
        ":pyasn1",
    ],
)

pip_library(
    name = "google-auth",
    version = "1.35.0",
    deps = [
        ":cachetools",
        ":pyasn1-modules",
        ":rsa",
        ":setuptools",
        ":six",
    ],
)

pip_library(
    name = "oauthlib",
    version = "3.1.1",
)

pip_library(
    name = "requests",
    version = "2.22.0",
)

pip_library(
    name = "setuptools",
    version = "25.2.0",
)

pip_library(
    name = "requests-oauthlib",
    version = "1.3.0",
    deps = [
        ":oauthlib",
        ":requests",
    ],
)

pip_library(
    name = "google-auth-oauthlib",
    version = "0.4.6",
    deps = [
        ":google-auth",
        ":requests-oauthlib",
    ],
)

pip_library(
    name = "Markdown",
    version = "3.3.4",
)

pip_library(
    name = "tensorboard-data-server",
    version = "0.6.1",
)

pip_library(
    name = "tensorboard-plugin-wit",
    version = "1.8.0",
)

pip_library(
    name = "Werkzeug",
    version = "2.0.1",
)

pip_library(
    name = "tensorboard",
    version = "2.6.0",
    deps = [
        ":absl-py",
        ":google-auth",
        ":google-auth-oauthlib",
        ":grpcio",
        ":Markdown",
        ":numpy",
        ":protobuf",
        ":requests",
        ":setuptools",
        ":tensorboard-data-server",
        ":tensorboard-plugin-wit",
        ":Werkzeug",
        ":wheel",
    ],
)

pip_library(
    name = "tensorflow-estimator",
    version = "2.6.0",
)

pip_library(
    name = "termcolor",
    version = "1.1.0",
)

pip_library(
    name = "typing-extensions",
    version = "3.7.4.3",
)

pip_library(
    name = "wrapt",
    version = "1.12.1",
)

pip_library(
    name = "tensorflow",
    version = "2.5.0",
    deps = [
        ":absl-py",
        ":astunparse",
        ":clang",
        ":flatbuffers",
        ":gast",
        ":google-pasta",
        ":grpcio",
        ":h5py",
        ":keras",
        ":Keras-Preprocessing",
        ":opt-einsum",
        ":protobuf",
        ":six",
        ":tensorboard",
        ":tensorflow-estimator",
        ":termcolor",
        ":typing-extensions",
        ":wheel",
        ":wrapt",
    ],
)
