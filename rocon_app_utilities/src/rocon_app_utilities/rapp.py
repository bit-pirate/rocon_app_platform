#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_app_platform/license/LICENSE
#
#################################################################################

from __future__ import division, print_function 

import yaml

class Rapp(object):
    # TODO Add public_paremters and rename interface to public_interface
    _required_attribute = ['display', 'description', 'compatibility', 'interface', 'launch']

    _optional_attribute = ['icon', 'paired_clients', 'required_capability']
    _parent_attribute = 'parent_specification'

    def __init__(self, filename=None):
        self.data = {}

        if filename:
            self.load_from_file(filename)

    def load_from_file(self, filename):
        '''
            Load rapp specs from the given file 
        '''
        with open(filename, 'r') as f:
            data = {}
            app_data = yaml.load(f.read())

            for ra in self._required_attribute:
                if ra in app_data:
                    data[ra] = app_data[ra]
                else:
                    valid = False
            for oa in self._optional_attribute:
                if oa in app_data:
                    data[oa] = app_data[oa]
            if self._parent_attribute in app_data:
                data[self._parent_attribute] = app_data[self._parent_attribute]

            self.data = data

        return self.validate()

    def get_parent(self):
        return self.data[self._parent_attribute]

    def validate(self):
        '''
            Validate whether the rapp has all required attributes.
            and returns missing required attributes

            @return missing required_attributes
            @rtype []
        '''
        missing_required_attributes = set(self._required_attribute).difference(set(self.data.keys()))

        return missing_required_attributes

class MetaRapp(Rapp):
    # TODO Add public_paremters and rename interface to public_interface
    _required_attribute = ['display', 'description', 'compatibility', 'interface']
    _optional_attribute = ['icon', 'paired_clients']
