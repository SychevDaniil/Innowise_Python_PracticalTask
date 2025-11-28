from config import OUTPUT_DIR
import json
import xml.etree.ElementTree as ET


def export_json(data, report_name):

    OUTPUT_DIR.mkdir(exist_ok=True)
    # превращаем список кортежей в список словарей
    result = [dict(zip([desc[0] for desc in data["description"]], row)) for row in data["rows"]]

    with open(OUTPUT_DIR / f"{report_name}.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

def export_xml(data, report_name):
    OUTPUT_DIR.mkdir(exist_ok=True)

    # создаём корневой элемент
    root = ET.Element("Report")

    # для каждой строки формируем элемент <Row>
    col_names = [desc[0] for desc in data["description"]]
    for row in data["rows"]:
        row_elem = ET.SubElement(root, "Row")
        for col_name, value in zip(col_names, row):
            col_elem = ET.SubElement(row_elem, col_name)
            col_elem.text = str(value)

    # сохраняем в файл
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    tree.write(OUTPUT_DIR / f"{report_name}.xml", encoding="utf-8", xml_declaration=True)