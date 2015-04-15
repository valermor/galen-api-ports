/****************************************************************************
 * Copyright 2015 Valerio Morsella                                          *
 *                                                                          *
 * Licensed under the Apache License, Version 2.0 (the "License");          *
 * you may not use this file except in compliance with the License.         *
 * You may obtain a copy of the License at                                  *
 *                                                                          *
 *    http://www.apache.org/licenses/LICENSE-2.0                            *
 *                                                                          *
 * Unless required by applicable law or agreed to in writing, software      *
 * distributed under the License is distributed on an "AS IS" BASIS,        *
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. *
 * See the License for the specific language governing permissions and      *
 * limitations under the License.                                           *
 ****************************************************************************/

package galen.api.server.utils;

import com.google.common.base.Predicate;
import com.google.common.collect.Iterables;
import galen.api.server.GalenReportsContainer;
import galen.api.server.thrift.ReportNode;
import galen.api.server.thrift.ReportTree;
import net.mindengine.galen.reports.TestReport;
import net.mindengine.galen.reports.nodes.TestReportNode;
import net.mindengine.galen.reports.nodes.TextReportNode;

import static galen.api.server.thrift.NodeType.LAYOUT;
import static galen.api.server.thrift.NodeType.TEXT;


public class TestReportUtils {

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
        return Iterables.filter(reportTree.getNodes(), new Predicate<ReportNode>() {
            @Override
            public boolean apply(ReportNode node) {
                return node.getParent_id().equals(parentNodeUniqueId);
            }
        });
    }

    private static void processLeaf(ReportNode node, TestReport testReport) {
        switch (node.getNode_type()) {
            case LAYOUT:
                testReport.layout(GalenReportsContainer.get().fetchLayoutReport(node.unique_id), node.getName());
                break;
            case TEXT:
                break;
            case NODE:
                if (node.getNode_type().equals(LAYOUT)) {
                    testReport.layout(GalenReportsContainer.get().fetchLayoutReport(node.unique_id), node.getName());
                } else if (node.getNode_type().equals(TEXT)) {
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
