namespace java net.skyscanner.galen.api
namespace py galenthrift

service Properties {
	string getProperty(1:string key, 2:string defaultValue)
}