from PyQt5 import QtWidgets
import syntax_pars

app = QtWidgets.QApplication([])
editor = QtWidgets.QTextEdit()
editor.setStyleSheet("""QPlainTextEdit{
	font-family:'Consolas'; 
	color: #ccc; 
	background-color: #ffffff;}""")
highlight = syntax_pars.PythonHighlighter(editor.document())
editor.show()

# Load syntax.py into the editor for demo purposes


app.exec_()