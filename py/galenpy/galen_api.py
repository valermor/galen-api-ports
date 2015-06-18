############################################################################
# Copyright 2015 Valerio Morsella                                          #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#    http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################

import logging

from exception import IllegalMethodCallException, FileNotFoundError
from galenpy.galen_webdriver import GalenRemoteWebDriver
from galenpy.thrift_client import ThriftClient
from pythrift.ttypes import SpecNotFoundException


logger = logging.getLogger()


class Galen(object):
    """
    Galen API class.

    Example usage.
    driver = GalenWebDriver("http://localhost:4444/wd/hub", desired_capabilities=CHROME)
    driver.get("http://example.com")
    driver.set_window_size(720, 1024)

    galen_api = Galen()
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
        if not isinstance(driver, GalenRemoteWebDriver):
            raise ValueError("Provided driver object is not an instance of GalenWebDriver")
        self.thrift_client = driver.thrift_client
        try:
            return self.thrift_client.check_layout(driver.session_id, spec, included_tags, excluded_tags)
        except SpecNotFoundException as e:
            raise IOError("Spec was not found: " + str(e.message))

    def generate_report(self, report_folder):
        """
        Generate Galen reports in the provided folder.
        :param report_folder: target folder.
        """
        if not self.thrift_client:
            raise IllegalMethodCallException("generate_report() must be called after check_layout()")
        logger.info("Generating reports in " + report_folder)
        self.thrift_client.generate_report(report_folder)
        self.thrift_client.quit_service_if_inactive()


def generate_galen_report(report_folder):
    thrift_client = ThriftClient()
    Galen(thrift_client).generate_report(report_folder)
