import uuid

from galenapi.pythrift.ttypes import ReportTree, NodeType, ReportNode


INFO = "info"
WARN = "warn"
ERROR = "error"


class TestReport(object):

    def __init__(self, thrift_client, test_name):
        super(TestReport, self).__init__()
        self.test_name = test_name
        self.report = ReportTree(root_id=generate_random_string())
        self.report.nodes = {}
        self.thrift_client = thrift_client

        thrift_client.register_test(test_name)

    def add_report_node(self, node_tree_builder):
        node_tree = node_tree_builder.build()
        self._add_node_tree(node_tree, self.report.root_id)
        return self

    def add_layout_report_node(self, name, report_node):
        report_node.name = name
        report_node.parent_id = self.report.root_id
        report_node.nodes_ids = []
        self.report.nodes[report_node.unique_id] = report_node
        return self

    def _add_node_tree(self, node_tree, parent_id):
        if node_tree.has_children():
            for node in node_tree.children:
                self._add_node_tree(node, node_tree.unique_id)
            self.report.nodes[node_tree.unique_id] = ReportNode(node_tree.unique_id, node_tree.name, node_tree.status,
                                                                parent_id, [c.unique_id for c in node_tree.children],
                                                                node_tree.attachment, node_tree.time,
                                                                node_tree.node_type)

        else:
            self.report.nodes[node_tree.unique_id] = ReportNode(node_tree.unique_id, node_tree.name, node_tree.status,
                                                                parent_id, [],  node_tree.attachment, node_tree.time,
                                                                node_tree.node_type)

    def finalize(self):
        self.thrift_client.finalize(self.test_name, self.report)

    def __str__(self):
        final_string = "Report root_id: " + self.report.root_id + "\n"
        for node_key in self.report.nodes.keys():
            final_string += "has node with id: " + self.report.nodes[node_key].unique_id + "\n"
            final_string += repr(self.report.nodes[node_key]) + "\n"
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
