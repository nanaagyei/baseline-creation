import sys
from PyQt5.QtWidgets import QApplication, QButtonGroup, QGroupBox, QRadioButton, QMainWindow, QTabWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QMenuBar, QMenu, QFileDialog, QHBoxLayout, QTabBar, QFrame, QWidget
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OPUS PROJECT BASELINE GENERATOR")

        # # Set the window icon
        # icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        # self.setWindowIcon(QIcon(icon_path))

        # Set the size and position of the window
        self.resize(800, 600)
        self.move(100, 100)

        # Create a menu bar
        self.menu_bar = QMenuBar()

        # Create a menu for the File tab
        self.file_menu = QMenu("File")
        self.menu_bar.addMenu(self.file_menu)

        # Create a menu item to open a file
        self.open_action = QAction("Open", self)
        self.open_action.triggered.connect(self.open_file)
        self.file_menu.addAction(self.open_action)

        # Create a menu item to open a folder
        self.open_folder_action = QAction("Open Folder", self)
        self.open_folder_action.triggered.connect(self.open_folder)
        self.file_menu.addAction(self.open_folder_action)

        # Create a menu item to save a file
        self.save_action = QAction("Save", self)
        self.save_action.triggered.connect(self.save_file)
        self.file_menu.addAction(self.save_action)

        # Create a menu for the View tab
        self.view_menu = QMenu("View")
        self.menu_bar.addMenu(self.view_menu)

        # Set the menu bar as the main window's menu bar
        self.setMenuWidget(self.menu_bar)

        # Create a tab widget
        self.tab_widget = QTabWidget()

        # Create a tab for the home page
        self.home_tab = QWidget()
        self.tab_widget.addTab(self.home_tab, "Home")

        # Create a group box for the project type radio buttons
        self.project_type_group_box = QGroupBox("Project Type")
        self.project_type_group_box.setAlignment(Qt.AlignCenter)

        # Create a button group for the radio buttons
        self.project_type_button_group = QButtonGroup()

        # Create a radio button for the pipeline project
        self.pipeline_radio_button = QRadioButton("Pipeline")
        self.pipeline_radio_button.setChecked(True)
        self.project_type_button_group.addButton(self.pipeline_radio_button)

        # Create a radio button for the facility project
        self.facility_radio_button = QRadioButton("Facility")
        self.project_type_button_group.addButton(self.facility_radio_button)

        # Add the radio buttons to the group box
        self.project_type_layout = QVBoxLayout()
        self.project_type_layout.addWidget(self.pipeline_radio_button)
        self.project_type_layout.addWidget(self.facility_radio_button)
        self.project_type_group_box.setLayout(self.project_type_layout)

        # Create a combo box for the project list
        self.project_combo_box = QComboBox()
        self.project_combo_box.addItems(["Project 1", "Project 2", "Project 3"])

        # Create a push button for generating the report
        self.generate_report_button = QPushButton("Generate Report")
        self.generate_report_button.clicked.connect(self.generate_report)

        # Add the group box and push button to the home tab layout
        self.home_tab_layout = QVBoxLayout()
        self.home_tab_layout.addWidget(self.project_type_group_box)
        self.home_tab_layout.addWidget(self.project_combo_box)
        self.home_tab_layout.addWidget(self.generate_report_button)
        self.home_tab.setLayout(self.home_tab_layout)
        # Create a tab for the map page
        self.map_tab = QWidget()
        self.tab_widget.addTab(self.map_tab, "Map")

        # Create a web view widget for the map
        self.map_web_view = QWebEngineView()
        self.map_web_view.load(QUrl("https://www.openstreetmap.org/"))

        # Add the web view widget to the map tab layout
        self.map_tab_layout = QVBoxLayout()
        self.map_tab_layout.addWidget(self.map_web_view)
        # Create a tab for the report page
        self.report_tab = QWidget()
        self.tab_widget.addTab(self.report_tab, "Report")

        # Create a label for the report
        self.report_label = QLabel("No report available")

        # Create a push button for viewing the report
        self.view_report_button = QPushButton("View Report")
        self.view_report_button.clicked.connect(self.view_report)

        # Add the label and push button to the report tab layout
        self.report_tab_layout = QVBoxLayout()
        self.report_tab_layout.addWidget(self.report_label)
        self.report_tab_layout.addWidget(self.view_report_button)
        self.report_tab.setLayout(self.report_tab_layout)

        # Set the tab widget as the central widget of the main window
        self.setCentralWidget(self.tab_widget)

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            print(f"Opening file: {file_name}")

    def open_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        folder_name = QFileDialog.getExistingDirectory(self, "Open Folder", options=options)
        if folder_name:
            print(f"Opening folder: {folder_name}")

    def save_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            print(f"Saving file: {file_name}")

    def zoom_in(self):
        print("Zooming in")

    def zoom_out(self):
        print("Zooming out")

    def pan(self):
        print("Panning")

    def zoom_to_extent(self):
        print("Zooming to extent")

    def generate_report(self):
        project_type = "Pipeline" if self.pipeline_radio_button.isChecked() else "Facility"
        project_name = self.project_combo_box.currentText()
        print(f"Generating report for {project_type} project: {project_name}")

    def view_report(self):
        print("Viewing report")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()