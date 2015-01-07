namespace java net.skyscanner.galen.api
namespace py galenthrift

typedef string request_params


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
    void initialize(1:string remote_server_addr)
    Response execute(1:string command, 2:request_params params);
}