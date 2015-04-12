/***************************************************************************
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
 ***************************************************************************/

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
	3:map<string, string> map_cap
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
    2:list<ReportNode> nodes
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
