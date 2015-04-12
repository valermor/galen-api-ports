############################################################################
# Copyright 2015 Valerio Morsella                                          #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#    http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################

import uuid
from galenpy.pythrift.ttypes import ReportTree, ReportNode, NodeType
from galenpy.thrift_client import ThriftClient


INFO = "info"
WARN = "warn"
ERROR = "error"


class TestReport(object):
    def __init__(self, test_name, thrift_client=None):
        super(TestReport, self).__init__()
        self.test_name = test_name
        self.report = ReportTree(root_id=generate_random_string())
        self.report.nodes = []
        self.thrift_client = thrift_client
        if not self.thrift_client:
            self.thrift_client = ThriftClient()

        self.thrift_client.register_test(test_name)

    def add_report_node(self, node_tree_builder):
        node_tree = node_tree_builder.build()
        self._add_node_tree(node_tree, self.report.root_id)
        return self

    def add_layout_report_node(self, name, layout_report):
        self.report.nodes.append(
            ReportNode(unique_id=layout_report.unique_id, name=name, parent_id=self.report.root_id, nodes_ids=[],
                       node_type=NodeType.LAYOUT))
        return self

    def _add_node_tree(self, node_tree, parent_id):
        if node_tree.has_children():
            for node in node_tree.children:
                self._add_node_tree(node, node_tree.unique_id)
            self.report.nodes.append(ReportNode(node_tree.unique_id, node_tree.name, node_tree.status, parent_id,
                                                 [c.unique_id for c in node_tree.children], node_tree.attachment,
                                                 node_tree.time, node_tree.node_type))

        else:
            self.report.nodes.append(
                ReportNode(node_tree.unique_id, node_tree.name, node_tree.status, parent_id, [], node_tree.attachment,
                           node_tree.time, node_tree.node_type))

    def finalize(self):
        self.thrift_client.finalize(self.test_name, self.report)

    def __str__(self):
        final_string = "Report root_id: " + self.report.root_id + "\n"
        for node in self.report.nodes:
            final_string += "has node with id: " + node.unique_id + "\n"
            final_string += repr(node) + "\n"
        return final_string


def info_node(name):
    return NodeBuilder().with_name(name).with_status(INFO)


def warn_node(name):
    return NodeBuilder().with_name(name).with_status(WARN)


def error_node(name):
    return NodeBuilder().with_name(name).with_status(ERROR)


class NodeBuilder(object):
    def __init__(self):
        super(NodeBuilder, self).__init__()
        self.name = None
        self.status = INFO
        self.attachment = None
        self.time = None
        self.node_type = NodeType.NODE
        self.children_nodes = []

    def with_name(self, name):
        self.name = name
        return self

    def with_status(self, status):
        self.status = status
        return self

    def with_attachment(self, attachment):
        self.attachment = attachment
        return self

    def with_node(self, node_builder):
        node = node_builder.build()
        self.children_nodes.append(node)
        return self

    def with_time(self, time):
        self.time = time
        return self

    def with_type(self, node_type):
        self.node_type = node_type
        return self

    def build(self):
        return Node(self.name, self.status, self.attachment, self.time, self.children_nodes, self.node_type)


class Node(object):
    def __init__(self, name, status, attachment, time, child_nodes, node_type=NodeType.NODE):
        self.unique_id = generate_random_string()
        self.name = name
        self.status = status
        self.attachment = attachment
        self.time = time
        self.node_type = node_type
        self.children = []
        self.children.extend(child_nodes)

    def has_children(self):
        return len(self.children) > 0


class TextNodeBuilder(NodeBuilder):
    def __init__(self):
        super(TextNodeBuilder, self).__init__()


def generate_random_string():
    return str(uuid.uuid4()).replace('-', '')
