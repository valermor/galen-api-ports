import os.path
import re
import unittest

from galenapi.galen_api import GalenApi, logger
from galenapi.galen_webdriver import GalenWebDriver
from galenapi.utils.specs import from_specs_in_current_folder


PROJECT_NAME = 'py'

CHROME = {
    "browserName": "chrome",
    "version": "",
    "platform": "ANY"
}


class HomePageLayoutTest(unittest.TestCase):
    """
    Example of layout test.
    """
    def test_home_page(self):
        driver = None
        try:
            driver = GalenWebDriver("http://localhost:4444/wd/hub", desired_capabilities=CHROME)
            driver.get("http://galenframework.com/")
            driver.set_window_size(1024, 724)

            galen_api = GalenApi().with_test_info('a Galen test')
            errors = galen_api.check_layout(driver, from_specs_in_current_folder('specs').with_name('homePage.spec'),
                                            ['tablet', 'all'], None)
            if errors != 0:
                galen_api.generate_report(get_target_dir(PROJECT_NAME, "target/galen"))
        except Exception as e:
            logger.error(e.message)
            raise e
        finally:
            driver.quit()


def get_target_dir(project_name, target_dir):
    project_path = '(.*/' + project_name + ').*'
    p = re.compile(project_path)
    m = p.match(os.getcwd())
    if m.groups():
        return os.path.join(m.groups()[0], target_dir)
