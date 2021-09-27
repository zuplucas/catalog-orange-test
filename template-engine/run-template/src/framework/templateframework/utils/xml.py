
from xml.etree import ElementTree as et


# Todo evoluir logica
class XMLCombiner(object):
    def __init__(self, filenames):
        ns = "http://maven.apache.org/POM/4.0.0"
        et.register_namespace('', ns)
        self.roots = [et.parse(f).getroot() for f in filenames]

    def combine(self):
        for r in self.roots[1:]:
            self.combine_element(self.roots[0], r)
        return et.tostring(self.roots[0])

    def combine_element(self, one, other):
        mapping = {el.tag: el for el in one}
        for el in other:
            if mapping.get(el.tag) is None:
                one.append(el)
                continue
            if len(el) == 0:
                one.append(el)
            else:
                have_artifact_id = False
                for children in el:
                    if 'artifactId' in children.tag:
                        have_artifact_id = True
                if have_artifact_id:
                    one.append(el)
                else:
                    self.combine_element(mapping[el.tag], el)

    def merge_dependencies(self, one, other):
        dependency_by_artifact_id = {}
        for dependency in one:
            for el in dependency:
                if "artifactId" in el.tag:
                    dependency_by_artifact_id[el.text] = dependency
        for dependency in other:
            for el in dependency:
                if "artifactId" in el.tag:
                    if dependency_by_artifact_id.get(el.text) is None:
                        one.append(dependency)

    def merge_build(self, one, other):
        plugin_by_artifact_id = {}
        for one_build in one:
            for plugins in one_build:
                for el in plugins:
                    if "artifactId" in el.tag:
                        plugin_by_artifact_id[el.text] = el
            for other_build in other:
                for plugins in other_build:
                    for el in plugins:
                        if "artifactId" in el.tag:
                            if plugin_by_artifact_id.get(el.text) is None:
                                one_build.append(el)
