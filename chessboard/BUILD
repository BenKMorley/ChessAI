python_library(
  name = "chessboard",
  srcs = [
    "chessboard.py",
  ],
  visibility = [
    "PUBLIC"
  ],
  deps = [
    "//chessboard/pieces:pieces",
    "//third_party/python:numpy",
  ],
)

python_test(
  name = "chessboard_test",
  srcs = [
    "chessboard_test.py",
  ],
  deps = [
    ":chessboard",
  ]
)