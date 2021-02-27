python_library(
  name = "chessboard",
  srcs = [
    "chessboard.py",
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
  name = "chessboard_test",
  srcs = [
    "chessboard_test.py",
    "pieces_test.py",
  ],
  deps = [
    ":chessboard",
  ]
)