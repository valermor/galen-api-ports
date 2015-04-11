package galen.api.server;

import com.google.common.collect.Lists;
import galen.api.server.thrift.NodeType;
import galen.api.server.thrift.ReportNode;
import galen.api.server.thrift.ReportTree;
import galen.api.server.utils.ReportUtils;
import net.mindengine.galen.reports.TestReport;
import net.mindengine.galen.reports.nodes.TestReportNode;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.is;

public class GalenReportCreationTest {

    public static final String firstNodeId = "1";
    public static final String secondNodeId = "2";
    public static final String thirdNodeId = "3";
    public static final String fourthNodeId = "4";
    public static final String fifthNodeId = "5";
    public static final String sixthNodeId = "6";

    private ReportTree reportTree;
    private String rootId = "rootId";

    private static final List<String> emptyList = Lists.newArrayList();

    /**
     * Structure of the sample tree for testing.
     *
     *          root
     *        /      \
     *       1e       2i
     *      / \      /
     *     3i  4w   5w
     *              |
     *              6e
     *
     *
     */
  @BeforeMethod
    public void setUp() throws Exception {
        Map<String, ReportNode> nodes = new HashMap<String, ReportNode>();
        nodes.put(firstNodeId, new ReportNode(firstNodeId, "first node", "error", rootId, Lists.newArrayList(thirdNodeId,
                fourthNodeId), null, new Date().toString(), NodeType.NODE));
        nodes.put(secondNodeId, new ReportNode(secondNodeId, "second node", "info", rootId, Lists.newArrayList(fifthNodeId),
                null, new Date().toString(), NodeType.NODE));
        nodes.put(thirdNodeId, new ReportNode(thirdNodeId, "third node", "info", firstNodeId, emptyList, null, new Date().toString(), NodeType.NODE));
        nodes.put(fourthNodeId, new ReportNode(fourthNodeId, "fourth node", "warn", firstNodeId, emptyList, null, new Date().toString(), NodeType.NODE));
        nodes.put(fifthNodeId, new ReportNode(fifthNodeId, "fifth node", "warn", secondNodeId, Lists.newArrayList(sixthNodeId),
                null, new Date().toString(), NodeType.NODE));
        nodes.put(sixthNodeId, new ReportNode(sixthNodeId, "sixth node", "error", fifthNodeId, emptyList, null, new Date().toString(), NodeType.NODE));
        reportTree = new ReportTree(rootId, nodes);
    }

    @Test(enabled = false)
    public void reportHasAllNodesInCorrectOrder() throws Exception {
        TestReport testReport = new TestReport();
        ReportUtils.buildTestReportFromReportTree(testReport, reportTree, rootId);
        TestReportNode firstNode = testReport.getNodes().get(0);
        assertThat("Root node should have node 1 as first child", firstNode.getName(), is("first node"));
        TestReportNode secondNode = testReport.getNodes().get(1);
        assertThat("Root node should have node 2 as second child", secondNode.getName(), is("second node"));
        TestReportNode thirdNode = firstNode.getNodes().get(0);
        TestReportNode fourthNode = firstNode.getNodes().get(1);
        assertThat("first node should have node 3 as first child", thirdNode.getName(), is("third node"));
        assertThat("first node should have node 4 as second child", fourthNode.getName(), is("fourth node"));
        TestReportNode fifthNode = secondNode.getNodes().get(0);
        assertThat("second node should have node 5 as only child", fifthNode.getName(), is("fifth node"));
        TestReportNode sixthNode = fifthNode.getNodes().get(0);
        assertThat("fifth node should have node 6 as only child", sixthNode.getName(), is("sixth node"));
    }
}
