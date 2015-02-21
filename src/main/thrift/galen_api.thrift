namespace java net.skyscanner.galen.api
namespace py galenthrift

typedef list<string> spec_paths
typedef list<string> tags


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

service RemoteCommandExecutor {
    void initialize(1:string remote_server_addr),
    Response execute(1:string session_id, 2:string command, 3:string params),
    #void initialize_galen(1:string report_path),
    #i32 check_layout(1:string webdriver_session_id, 2:spec_paths specs, 3:tags included_tags, 4:tags excluded_tags, 5:string property_file_path)
}