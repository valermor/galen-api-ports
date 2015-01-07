namespace java galenthrift
namespace py galenthrift

union capability {
	1:string string_cap
	2:bool bool_cap
	3:set<string> set_cap
}

typedef map<string, capability> raw_caps
typedef map<string,string> request_params

service RemoteDriver {
    raw_caps initialize(1:string remote_server_addr, 2:raw_caps desired_caps)
    string execute(1:string command, 2:request_params params);
}