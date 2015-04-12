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

from os import path


class GalenSpecFinder(object):
    """
    Utility class with fluent methods to locate Galen specs in the file system.
    """
    def __init__(self):
        self.spec_folder = None

    def from_specs_in_current_folder(self, spec_folder_name):
        """
        Sets specs folder with provided name in the current directory.
        """
        return self.from_folder(path.join(path.abspath(path.curdir), spec_folder_name))

    def from_folder(self, spec_folder):
        """
        Sets specs folder to the provided directory path.
        """
        if path.isdir(spec_folder):
            self.spec_folder = spec_folder
        else:
            raise IOError(str(spec_folder) + " not found.")
        return self

    def with_name(self, spec_name):
        """
        Builds and return whole path to provided specs file.
        """
        full_path = path.join(self.spec_folder, spec_name)
        if path.exists(full_path):
            return full_path


def from_specs_in_current_folder(spec_folder_name):
    return GalenSpecFinder().from_specs_in_current_folder(spec_folder_name)
