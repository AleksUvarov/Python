import json
import csv
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from tkinter import filedialog
from tkinter import Tk

def html_to_json(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return json.dumps(soup.prettify())

def xml_to_json(xml_content):
    root = ET.fromstring(xml_content)
    return json.dumps({root.tag: xml_to_dict(root)})

def xml_to_html(content):
    try:
        root = ET.fromstring(content)
        html_output = "<!DOCTYPE html>\n<html>\n<head>\n<title>XML to HTML</title>\n</head>\n<body>\n"

        def parse_element(element):
            nonlocal html_output
            html_output += f"<{element.tag}>"
            for child in element:
                parse_element(child)
            html_output += f"</{element.tag}>"

        parse_element(root)

        html_output += "</body>\n</html>"
        return html_output

    except ET.ParseError as e:
        return f"Error parsing XML: {e}"

def xml_to_dict(element):
    result = {}
    for child in element:
        if child.tag in result:
            if isinstance(result[child.tag], list):
                result[child.tag].append(xml_to_dict(child))
            else:
                result[child.tag] = [result[child.tag], xml_to_dict(child)]
        else:
            result[child.tag] = xml_to_dict(child)
    return result

def csv_to_json(csv_content):
    csv_rows = csv.DictReader(csv_content.splitlines())
    return json.dumps(list(csv_rows))

def tsv_to_json(tsv_content):
    tsv_rows = csv.DictReader(tsv_content.splitlines(), delimiter='\t')
    return json.dumps(list(tsv_rows))

def json_to_html(json_content):
    data = json.loads(json_content)
    return "<html><body><pre>{}</pre></body></html>".format(json.dumps(data, indent=4))

def json_to_xml(json_content):
    data = json.loads(json_content)
    root_name = list(data.keys())[0]
    root = ET.Element(root_name)
    json_to_xml_recursive(data[root_name], root)
    return ET.tostring(root, encoding='unicode')

def json_to_xml_recursive(data, parent):
    if isinstance(data, dict):
        for key, value in data.items():
            element = ET.SubElement(parent, key)
            json_to_xml_recursive(value, element)
    elif isinstance(data, list):
        for item in data:
            json_to_xml_recursive(item, parent)
    else:
        parent.text = str(data)

def convert_format(content, input_format, output_format, output_file=None):
    if input_format == "HTML":
        if output_format == "JSON":
            output_data = html_to_json(content)
        elif output_format == "HTML":
            output_data = content
    elif input_format == "XML":
        if output_format == "JSON":
            output_data = xml_to_json(content)
        elif output_format == "HTML":
            output_data = xml_to_html(content) 
    elif input_format == "CSV":
        if output_format == "JSON":
            output_data = csv_to_json(content)
    elif input_format == "TSV":
        if output_format == "JSON":
            output_data = tsv_to_json(content)
    elif input_format == "JSON":
        if output_format == "HTML":
            output_data = json_to_html(content)
        elif output_format == "XML":
            output_data = json_to_xml(content)
    else:
        return "Unsupported conversion"

    if output_file:
        with open(output_file, 'w') as file:
            file.write(output_data)
    else:
        return output_data

# Пример использования:
input_content = """
{
    "person": {
        "name": "John",
        "age": 30,
        "city": "New York"
    }
}
"""

filename = input("Введите имя файла: ")
format_input = input("Введите формат файла (html, xml, csv, tsv, json): ")
format_output = input("Введите желаемый формат (html, xml, csv, tsv, json): ")
output_content = convert_format(input_content, format_input, format_output, filename)
print(output_content)
