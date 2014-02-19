#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_app_platform/license/LICENSE
#
#################################################################################

from __future__ import division, print_function 

import yaml

class MetaRapp(object):
    '''
        Class to handle Meta rapp
    '''
    # TODO Add public_paremters and rename interface to public_interface
    _required_attribute = ['display', 'description', 'interface']
    _optional_attribute = ['icon', 'paired_clients']
    _inheritable_attribute = ['display', 'description', 'interface', 'icon', 'paired_clients']
    # _parent_attribute : Meta Rapp does not have parent_specification

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

            self.load_inherits(data, app_data)



            self.data = data

        return self.validate()


    def load_inherits(self, data, app_data):
        '''
            Hook to parse extra information in file. It is called in load_from_file
        '''
        return None

    
    def validate(self):
        '''
            Validate whether the rapp has all required attributes.
            and returns missing required attributes

            @return missing required_attributes
            @rtype []
        '''
        missing_required_attributes = list(set(self._required_attribute).difference(set(self.data.keys())))
        return missing_required_attributes

    def get_parent(self):
        '''
            Meta rapp does not have parent. This function is to override Rapp class
        '''
        return None

    def get_inheritable_attributes(self):
        return {}





class Rapp(MetaRapp):
    # TODO Add public_paremters and rename interface to public_interface
    _required_attribute = ['display', 'description', 'compatibility', 'interface', 'launch']
    _optional_attribute = ['icon', 'paired_clients', 'required_capability']
    _parent_attribute = 'parent_specification'
    # _inheritable_attribute : inherited from MetaRapp

    def get_parent(self):
        '''
            @return the parent rapp name
            @rtype str
        '''
        if self._parent_attribute in self.data:
            return self.data[self._parent_attribute]
        else:
            return None

    def load_inherits(self, data, app_data):
        '''
            Hook to parse extra information in file. It is called in load_from_file
        '''
        if self._parent_attribute in app_data:
            data[self._parent_attribute] = app_data[self._parent_attribute].strip()

    def inherits(self):
        pass
