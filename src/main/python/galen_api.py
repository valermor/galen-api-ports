from exception import NotReadyException
from galen_webdriver import GalenWebDriver, CHROME


class GalenApi(object):

    def __init__(self):
        self.test_info = None
        self.thrift_client = None

    def with_test_info(self, test_info):
        self.test_info = test_info

    def check_layout(self, driver, spec, included_tags, excluded_tags):
        if not isinstance(driver, GalenWebDriver):
            raise ValueError("Provider driver object is not an instance of GalenWebDriver")
        self.thrift_client = driver.thrift
        self.thrift_client.check_api(self.test_info, driver.session_id, spec, included_tags, excluded_tags)

    def generate_report(self, report_folder):
        if not self.thrift_client:
            raise NotReadyException("generate_report() must be called after check_layout()")
        self.thrift_client.generate_report(report_folder)


def run_galen_test():
    driver = GalenWebDriver("http://localhost:4444/wd/hub", desired_capabilities=CHROME)
    driver.get("http://www.skyscanner.net/hotels")
    driver.set_window_size(720, 1024)

    galen_api = GalenApi()
    galen_api.with_test_info('a Galen test')
    galen_api.check_layout(driver, 'homePage.spec', ['phone'], None)
    galen_api.generate_report("target/galen")


if __name__ == '__main__':
    run_galen_test()