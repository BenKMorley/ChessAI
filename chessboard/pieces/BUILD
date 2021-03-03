python_library(
  name = "pieces",
  srcs = [
    "pieces.py"
  ],
  visibility = [
    "PUBLIC"
  ],
  deps = [
    "//third_party/python:numpy",
  ],
)

python_test(
  name = "pieces_test",
  srcs = [
    "pieces_test.py",
  ],
  deps = [
    ":pieces",
  ]
)