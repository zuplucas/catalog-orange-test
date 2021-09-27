from pathlib import Path
from unittest import TestCase

from templateframework.utils.xml import XMLCombiner


class TestXml(TestCase):
    def test_xml_merge_merge_dependency(self):
        f1 = Path("test_data/xml/merge_dependency/pom.xml")
        f2 = Path("test_data/xml/merge_dependency/pom_merge.xml")
        r = XMLCombiner((f1, f2)).combine()
        result_path = Path("test_data/xml/merge_dependency/result.xml")
        result_path.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n' +
            r.decode("utf-8"))

    def test_xml_merge_merge_plugin(self):
        f1 = Path("test_data/xml/merge_plugin/pom.xml")
        f2 = Path("test_data/xml/merge_plugin/pom_merge.xml")
        r = XMLCombiner((f1, f2)).combine()
        result_path = Path("test_data/xml/merge_plugin/result.xml")
        result_path.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n' +
            r.decode("utf-8"))
