#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_app_platform/license/LICENSE
#
#################################################################################

from __future__ import division, print_function 
import yaml

from .exceptions import InvalidRappException, InvalidFieldException

IMPLEMETATION_VALIDATION_LIST = ['launch', 'compatibility']
CHILD_VALIDATION_LIST = ['parent_specification']

class Rapp(object):

    _attributes = ['display', 'description', 'icon', 'public_interface', 'public_parameters', 'compatibility', 'launch', 'parent_specification', 'pairing_clients', 'required_capability']

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
            self.field_validation()
            self.classify()

    def field_validation(self):
        '''
            Validate each field. E.g) check rocon uri. Check the linked file exist 
        '''
        #  TODO
        pass

    def classify(self):
        '''
            Classify the current rapp among VirtualAncestor, ImplementationAnacestor, ImplementationChild 
        '''
        is_impl = self.is_implementation()
        is_ance = self.is_ancestor()

        impl = 'Implementation' if is_impl else 'Virtual'
        ance = 'Ancestor' if is_ance else 'Child'
        try:
            if is_impl and is_ance: # Implementation Ancestor
                ImplementationAncestorRapp.is_valid(self.data)
            elif is_impl and not is_ance: # Implementation Child
                ImplementationChildRapp.is_valid(self.data)
            elif not is_impl and is_ance: # Virtual Ancestor
                VirtualAncestorRapp.is_valid(self.data)
            else:                         # Virtual Child
                raise InvalidRappException('Virtual Child rapp. Invalid!')
        except InvalidFieldException as ife:
            raise InvalidRappException('[' + impl + ' ' + ance + '] ' + str(ife))

        self.type = impl + ' ' + ance

            
    def is_implementation(self):
        '''
            It is implementation if it contains compatibility and launch attributes
        '''
        r = set(IMPLEMETATION_VALIDATION_LIST)
        m = set(self.data.keys())

        return r.issubset(m)

    def is_ancestor(self):
        '''
            It is ancestor rapp if it does not have parent_specification attribute
        '''
        r = set(CHILD_VALIDATION_LIST)
        m = set(self.data.keys())
        return (not r.issubset(m))


class RappValidation(Rapp):
    _required = []
    _optional = []
    _not_allowed = []
    _inherit = []

    @classmethod
    def is_valid(cls, data):

        missing_required = cls._difference(cls._required, data.keys()) 
        included_not_allowed = cls._intersection(cls._not_allowed, data.keys())

        if len(missing_required) > 0 or len(included_not_allowed) > 0:
            raise InvalidFieldException(missing_required, included_not_allowed)
        
        return False

    @classmethod
    def _intersection(cls, attributes, data):
        intersection = set(attributes).intersection(set(data))
        return list(intersection)

    @classmethod
    def _difference(cls, attributes, data):
        diff = set(attributes).difference(set(data))
        return list(diff)



class VirtualAncestorRapp(RappValidation):
    _required = ['display', 'description', 'public_interface', 'public_parameters']
    _optional = ['icon']
    _not_allowed = ['compatibility', 'launch', 'parent_specification', 'pairing_clients', 'required_capability']
    _inherit = []


class ImplementationAncestorRapp(RappValidation):
    _required = ['display', 'description', 'public_interface', 'public_parameters', 'compatibility', 'launch']
    _optional = ['icon', 'pairing_clients', 'required_capability']
    _not_allowed = ['parent_specification']
    _inherit = []


class ImplementationChildRapp(RappValidation):
    _required = ['compatibility', 'launch', 'parent_specification']
    _optional = ['icon', 'pairing_clients', 'required_capability']
    _not_allowed = ['public_interface', 'public_parameters']
    _inherit = ['display', 'description', 'icon', 'public_interface', 'public_parameters']
