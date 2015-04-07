package galen.api.server.utils;

import com.google.common.base.Predicate;
import com.google.common.collect.Iterables;
import galen.api.server.GalenReportsContainer;
import galen.api.server.thrift.NodeType;
import galen.api.server.thrift.ReportNode;
import galen.api.server.thrift.ReportTree;
import net.mindengine.galen.reports.TestReport;
import net.mindengine.galen.reports.nodes.TestReportNode;
import net.mindengine.galen.reports.nodes.TextReportNode;

import static galen.api.server.thrift.NodeType.LAYOUT;

public class ReportUtils {

    public static void buildTestReportFromReportTree(TestReport testReport, ReportTree reportTree, final String parentNodeUniqueId) {
        Iterable<ReportNode> childrenNodes = filterChildrenNodes(reportTree, parentNodeUniqueId);

        for (ReportNode node : childrenNodes) {
            if (node.getNodes_ids().size() == 0) {
                processLeaf(node, testReport);
            } else {
                processNode(node, testReport, reportTree);
            }
        }
    }

    private static Iterable<ReportNode> filterChildrenNodes(ReportTree reportTree, final String parentNodeUniqueId) {
        return Iterables.filter(reportTree.getNodes().values(), new Predicate<ReportNode>() {
            @Override
            public boolean apply(ReportNode node) {
                return node.getParent_id().equals(parentNodeUniqueId);
            }
        });
    }

    private static void processLeaf(ReportNode node, TestReport testReport) {
        switch (node.getType()) {
            case LAYOUT:
                testReport.layout(GalenReportsContainer.get().fetchLayoutReport(node.unique_id), node.getName());
                break;
            case TEXT:
                break;
            case NODE:
                if (node.getType().equals(LAYOUT)) {
                    testReport.layout(GalenReportsContainer.get().fetchLayoutReport(node.unique_id), node.getName());
                } else if (node.getType().equals(NodeType.TEXT)) {
                    testReport.addNode(new TextReportNode(testReport.getFileStorage(), node.name));
                } else {
                    if (node.getStatus().equals(TestReportNode.Status.INFO.toString())) {
                        testReport.info(node.getName());
                    } else if (node.getStatus().equals(TestReportNode.Status.WARN.toString())) {
                        testReport.warn(node.getName());
                    } else if (node.getStatus().equals(TestReportNode.Status.ERROR.toString())) {
                        testReport.error(node.getName());
                    }
                }
                break;

        }
    }

    private static void processNode(ReportNode node, TestReport testReport, ReportTree reportTree) {
        testReport.sectionStart(node.getName());
        buildTestReportFromReportTree(testReport, reportTree, node.getUnique_id());
        testReport.sectionEnd();
    }
}
