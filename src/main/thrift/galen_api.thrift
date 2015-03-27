namespace java galen.api.server.thrift
namespace py galenthrift

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

service GalenApiRemoteService {
	//WebDriver Remote Executor service
    void initialize(1:string remote_server_addr),
    Response execute(1:string session_id, 2:string command, 3:string params) throws (1:RemoteWebDriverException exc),

    //Galen API service
    i32 check_layout(1:string test_name, 2:string webdriver_session_id, 3:string specs, 4:tags included_tags, 5:tags excluded_tags) throws (1:SpecNotFoundException exc),
    void generate_report(1:string report_folder_path)

    //Service lifecycle
    i32 active_drivers()
    void shut_service()
}
