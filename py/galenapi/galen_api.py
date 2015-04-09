import logging

from exception import IllegalMethodCallException, FileNotFoundError
from galenapi.galen_webdriver import GalenWebDriver
from galenapi.thrift_client import ThriftFacade
from pythrift.ttypes import SpecNotFoundException


logger = logging.getLogger(__name__)


class GalenApi(object):
    """
    Galen API class.

    Example usage.
    driver = GalenWebDriver("http://localhost:4444/wd/hub", desired_capabilities=CHROME)
    driver.get("http://example.com")
    driver.set_window_size(720, 1024)

    galen_api = GalenApi().with_test_info('a Galen test')
    errors = galen_api.check_layout(driver, 'homePage.spec', ['phone'], None)
    if errors !=0:
        galen_api.generate_report("target/galen")
    """

    def __init__(self, thrift_client=None):
        self.thrift_client = thrift_client

    def check_layout(self, driver, spec, included_tags, excluded_tags):
        #TODO add multiple specs.
        """
        Main validation method.
        :param driver: An instance of GalenWebDriver.
        :param spec: Specs to be run on the page under test.
        :param included_tags: list of tags included in the check.
        :param excluded_tags: list of tags excluded from check.
        :return: CheckLayoutReport mapping info from the generated LayoutReport object in the Galen Server.
        """
        if not isinstance(driver, GalenWebDriver):
            raise ValueError("Provided driver object is not an instance of GalenWebDriver")
        self.thrift_client = driver.thrift_client
        try:
            return self.thrift_client.check_layout(driver.session_id, spec, included_tags, excluded_tags)
        except SpecNotFoundException as e:
            raise FileNotFoundError("Spec was not found: " + str(e.message))

    def generate_report(self, report_folder):
        """
        Generate Galen reports in the provided folder.
        :param report_folder: target folder.
        """
        if not self.thrift_client:
            raise IllegalMethodCallException("generate_report() must be called after check_layout()")
        logger.info("Generating reports in " + report_folder)
        self.thrift_client.generate_report(report_folder)
        self.thrift_client.shut_service_if_inactive()


def generate_galen_report(report_folder):
    thrift_client = ThriftFacade()
    GalenApi(thrift_client).generate_report(report_folder)
