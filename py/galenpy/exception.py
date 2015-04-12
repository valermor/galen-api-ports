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


class IllegalMethodCallException(Exception):
    """
    Thrown when a method is called on an object which is not in a right state.
    """
    def __init__(self, *args, **kwargs):
        super(IllegalMethodCallException, self).__init__(*args, **kwargs)


class FileNotFoundError(Exception):
    """
    A file was not found.
    """
    def __init__(self, *args, **kwargs):
        super(FileNotFoundError, self).__init__(*args, **kwargs)
