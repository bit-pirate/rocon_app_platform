#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_app_platform/license/LICENSE
#
#################################################################################

from __future__ import division, print_function 
import yaml

from .exceptions import InvalidRappException

class RappValidation(object):
    _required = []
    _optional = []
    _not_allowed = []
    _inherit = []

    def is_valid(self, data):
        if _contain(self.required, data):
            if not _contain(self._not_allowed, data):
                return True

        return False

    def _contain(self, attributes, data):

        intersection = set(attributes).intersection(set(data))

        return True if len(intersection) > 0 else False


class VirtualAncestorRapp(RappValidation):
    _required = ['display', 'description', 'public_interface', 'public_parameters']
    _optional = ['icon']
    _not_allowed = ['compatibility', 'launch', 'parent_specification', 'paired_clients', 'required_capability']
    _inherit = []


class ImplementationAncestorRapp(RappValidation):
    _required = ['display', 'description', 'public_interface', 'public_parameters', 'compatibility', 'launch']
    _optional = ['icon', 'paired_clients', 'required_capability']
    _not_allowed = ['parent_specification']
    _inherit = []


class ImplementationChildRapp(RappValidation):
    _required = ['compatibility', 'launch', 'parent_specification']
    _optional = ['icon', 'paired_clients', 'required_capability']
    _not_allowed = ['public_interface', 'public_parameters']
    _inherit = ['display', 'description', 'icon', 'public_interface', 'public_parameters']


class Rapp(object):

    _attributes = ['display', 'description', 'icon', 'public_interface', 'public_parameters', 'compatibility', 'launch', 'parent_specification', 'paired_clients', 'required_capability']

    def __init__(self, name, filename=None):
        self.name = name
        self.data = {}
        self.type = None

        if filename: 
            self.load_from_file(filename)


    def load_from_file(self, filename):
        '''
            Load rapp specs from the given file
        '''
        with open(filename, 'r') as f:
            app_data = yaml.load(f.read())

            for d in app_data:
                if d not in self._attributes:
                    raise InvalidRappException('Invalid Field : ' + str(d))

            self.data = app_data
            self.classify()

    def classify(self):
        '''
            Classify the current rapp among VirtualAncestor, ImplementationAnacestor, ImplementationChild 
        '''
        is_impl = self.is_implementation()
        is_ance = self.is_ancestor()

        if is_impl and is_ance: # Implementation Ancestor
            if ImplementationAncestorRapp.is_valid(self.data):
                self.type = ImplementationAnacestor
            else: 
                raise InvalidRappException('Implementation Ancestor Rapp Invalid')
        elif is_impl and not is_ance: # Implementation Child
            if ImplementationChildRapp.is_valid(self.data):
                self.type = ImplementationChildRapp
            else: 
                raise InvalidRappException('Implementation Child Rapp Invalid')
        elif not is_impl and is_ance: # Virtual Ancestor
            if VirtualAncestorRapp.is_valid(self.data):
                self.type = VirtualAncestorRapp
            else: 
                raise InvalidRappException('Virtual Ancetor Rapp Invalid')
        else:                         # Virtual Child
            raise InvalidRappException('Virtual Child rapp. Invalid!')
            

    def is_implementation(self):
        '''
            It is implementation if it contains compatibility and launch attributes
        '''
        r = set(['compatibility', 'launch'])
        m = set(self.data.keys())

        return r.issubset(m)

    def is_ancestor(self):
        '''
            It is ancestor rapp if it does not have parent_specification attribute
        '''
        return True if 'parent_specification' in self.data else False
