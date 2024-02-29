import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView



# Run the Qt application
app = QApplication(sys.argv)

# Create a QWebEngineView widget to display the HTML map
web_view = QWebEngineView()

# Load the HTML map file from a file path
file_path = r"D:\baseline creation\index_1.html"
web_view.load(QUrl.fromLocalFile(file_path))

# Create a main window and set the layout
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(web_view)
window.setLayout(layout)

# Show the main window
window.show()
sys.exit(app.exec())



# sys.exit(app.exec_())
# import sys
# from PySide6.QtCore import QUrl
# from PySide6.QtWebEngineWidgets import QWebEngineView
# import folium
# from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

# from PySide6.QtCore import QUrl
# from PySide6.QtWebEngineWidgets import QWebEngineView
# import folium

# # Create a QApplication object
# app = QApplication(sys.argv)

# # Create a map centered at the coordinates (50.0, -100.0)
# m = folium.Map(location=[50.0, -100.0], zoom_start=4)

# # Add a marker at the coordinates (50.0, -100.0)
# folium.Marker([50.0, -100.0]).add_to(m)

# # Save the map to an HTML file
# m.save('map.html')

# # Create a QWidget object
# window = QWidget()

# # Set the window title
# window.setWindowTitle('My Map')

# # Create a QWebEngineView widget to display the HTML map
# web_view = QWebEngineView(window)

# # Load the HTML map file from a file path
# file_path = r"map.html"
# web_view.load(QUrl.fromLocalFile(file_path))

# # Show the QWidget
# window.show()

# # Execute the application's event loop
# sys.exit(app.exec())


