from chessboard.chessboard import Chessboard

opt = 'qt'

if opt == 'tk':
    from renderer.tk.tk_renderer import display as tk_display
    a = Chessboard()
    tk_display(a)

if opt == 'qt':
    from renderer.qt5.qt5_renderer import display as qt_display
    a = Chessboard()
    qt_display(a)

if opt == 'mpl':
    from renderer.mpl.mpl_renderer import display as mpl_display
    a = Chessboard()
    mpl_display(a)
