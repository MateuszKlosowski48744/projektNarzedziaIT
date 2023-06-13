import sys
import json
import yaml
import xmltodict
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox


class DataConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konwerter Plikow")
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        self.input_file_label = QLabel("Plik wejsciowy:")
        self.input_file_edit = QLineEdit()
        self.browse_input_button = QPushButton("Szukaj")
        self.output_file_label = QLabel("Plik wyjsciowy:")
        self.output_file_edit = QLineEdit()
        self.browse_output_button = QPushButton("Szukaj")
        self.convert_button = QPushButton("Konwertuj")
        self.layout.addWidget(self.input_file_label)
        self.layout.addWidget(self.input_file_edit)
        self.layout.addWidget(self.browse_input_button)
        self.layout.addWidget(self.output_file_label)
        self.layout.addWidget(self.output_file_edit)
        self.layout.addWidget(self.browse_output_button)
        self.layout.addWidget(self.convert_button)
        self.browse_input_button.clicked.connect(self.browse_input_file)
        self.browse_output_button.clicked.connect(self.browse_output_file)
        self.convert_button.clicked.connect(self.convert_data)

    def browse_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik wejsciowy")
        self.input_file_edit.setText(file_path)

    def browse_output_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Wybierz plik wyjsciowy")
        self.output_file_edit.setText(file_path)

    def show_message(self, message):
        QMessageBox.information(self, "Message", message)
#konwertowanie xml na json
    def convert_xml_to_json(self, xml_data):
        return json.dumps(xmltodict.parse(xml_data), indent=4)
#konwertowanie json na xml
    def convert_json_to_xml(self, json_data):
        return xmltodict.unparse(json.loads(json_data), pretty=True)
#konwertowanie json na yamla
    def convert_json_to_yaml(self, json_data):
        return yaml.dump(json.loads(json_data), default_flow_style=False)
#konwertowanie yaml'a na json
    def convert_yaml_to_json(self, yaml_data):
        return json.dumps(yaml.safe_load(yaml_data), indent=4)

    def convert_data(self):
        input_file = self.input_file_edit.text()
        output_file = self.output_file_edit.text()

        if not input_file or not output_file:
            self.show_message("Prosze podać sciezki plików wejsciowych i wyjsciowych")
            return

        with open(input_file, 'r') as file:
            input_data = file.read()

        if input_file.endswith('.xml') and output_file.endswith('.json'):
            output_data = self.convert_xml_to_json(input_data)
        elif input_file.endswith('.xml') and output_file.endswith('.yaml'):
            json_data = self.convert_xml_to_json(input_data)
            output_data = self.convert_json_to_yaml(json_data)
        elif input_file.endswith('.json') and output_file.endswith('.xml'):
            output_data = self.convert_json_to_xml(input_data)
        elif input_file.endswith('.json') and output_file.endswith('.yaml'):
            output_data = self.convert_json_to_yaml(input_data)
        elif input_file.endswith('.yaml') and output_file.endswith('.xml'):
            json_data = self.convert_yaml_to_json(input_data)
            output_data = self.convert_json_to_xml(json_data)
        elif input_file.endswith('.yaml') and output_file.endswith('.json'):
            output_data = self.convert_yaml_to_json(input_data)
        else:
            self.show_message("Ten format plikow nie jest obslugiwany")
            return

        with open(output_file, 'w') as file:
            file.write(output_data)

        self.show_message("Konwersacja udana pomyslnie")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = DataConverter()
    converter.show()
    sys.exit(app.exec_())
