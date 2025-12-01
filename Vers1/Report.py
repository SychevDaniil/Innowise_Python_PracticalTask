from config import OUTPUT_DIR
import json
import os
import xml.etree.ElementTree as ET

class Report():
    def __init__(self, data_dir = OUTPUT_DIR):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def export_json(self, data, report_name):
        with open(self.data_dir / f"{report_name}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def export_xml(self, data, report_name):
        root = ET.Element("Report")
        for row in data:
            row_elem = ET.SubElement(root, "Row")
            for col_name, value in row.items():
                col_elem = ET.SubElement(row_elem, col_name)
                col_elem.text = str(value)

        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ", level=0)
        tree.write(self.output_dir / f"{report_name}.xml", encoding="utf-8", xml_declaration=True)

    def export(self, data, report_name, fmt="json"):
        if fmt == "json":
            self.export_json(data, report_name)
        elif fmt == "xml":
            self.export_xml(data, report_name)
        else:
            raise ValueError("Формат должен быть 'json' или 'xml'")