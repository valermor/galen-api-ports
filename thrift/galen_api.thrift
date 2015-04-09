namespace java galen.api.server.thrift
namespace py pythrift

typedef list<string> tags

exception SpecNotFoundException {
	1: string message
}

exception RemoteWebDriverException {
	1: string message
}

union ResponseValueType {
	1:string string_cap
	2:bool bool_cap
	3:set<string> set_cap
}

struct Response {
	1:ResponseValueType value
	2:string session_id
	3:i32 status
	4:string state
}

enum NodeType {
    NODE =1,
    LAYOUT = 2,
    TEXT = 3
}

struct ReportNode {
    1:string unique_id
    2:string name
    3:string status
    4:string parent_id
    5:list<string> nodes_ids
    6:list<string> attachment
    8:string time
    9:NodeType node_type
}

struct LayoutCheckReport {
    1:string unique_id
    4:i32 errors
    5:i32 warnings
}

struct ReportTree {
    1:string root_id,
    2:map<string, ReportNode> nodes
}


service GalenApiRemoteService {
	//WebDriver JsonWire over Thrift
    void initialize(1:string remote_server_addr),
    Response execute(1:string session_id, 2:string command, 3:string params) throws (1:RemoteWebDriverException exc),

    //Galen check and report API
    void register_test(1:string test_name),
    void append(1:string test_name, 2:ReportTree report_tree),
    LayoutCheckReport check_layout(1:string webdriver_session_id, 2:string specs, 3:tags included_tags, 4:tags excluded_tags) throws (1:SpecNotFoundException exc),
    void generate_report(1:string report_folder_path),

    //Service lifecycle
    i32 active_drivers(),
    void shut_service()
}
