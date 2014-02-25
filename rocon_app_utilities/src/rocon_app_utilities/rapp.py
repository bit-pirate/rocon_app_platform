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

#################################################################################
# Local Method
#################################################################################

def _is_implementation_rapp(data):
    '''
        It is implementation if it contains compatibility and launch attributes
    '''
    r = set(IMPLEMETATION_VALIDATION_LIST)
    m = set(data.keys())

    return r.issubset(m)

def _is_ancestor_rapp(data):
    '''
        It is ancestor rapp if it does not have parent_specification attribute
    '''
    r = set(CHILD_VALIDATION_LIST)
    m = set(data.keys())
    return (not r.issubset(m))


class Rapp(object):

    _attributes = ['display', 'description', 'icon', 'public_interface', 'public_parameters', 'compatibility', 'launch', 'parent_specification', 'pairing_clients', 'required_capability']
    _inheritable_attributes = ['display', 'description', 'icon', 'public_interface', 'public_parameters']

    def __init__(self, name, filename=None):
        self.name = name
        self.data = {}
        self.type = None

        if filename: 
            self.load_from_file(filename)

    def __str__(self):
        return str(self.name)


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

    def get_parent(self):
        '''
            @return Returns parent rapp name
            @rtype str 
        '''
        return self.data['parent_specification'] if 'parent_specification' in  self.data else None

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
        is_impl = _is_implementation_rapp(self.data)
        is_ance = _is_ancestor_rapp(self.data)

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
        self.is_impl = is_impl
        self.is_ance = is_ance

    def inherit(self, rapp):
        '''
            Inherits missing information from the given rapp
        '''
        for attribute in self._inheritable_attributes:
            if not attribute in self.data and attribute in rapp.data: 
                self.data[attribute] = rapp.data[attribute]

        self.classify()

    def is_implementation(self):
        return self.is_impl

    def is_ancestor(self):
        return self.is_ance


class RappValidation(Rapp):
    _required = []
    _optional = []
    _not_allowed = []

    @classmethod
    def is_valid(cls, data):
        '''
            Rapp Validation. If it has all requirements and does not include any not_allowed attributes, it is valid rapp
            
            @param rapp specification 
            @type dict

            @return 
            
        '''
        missing_required = cls._difference(cls._required, data.keys()) 
        included_not_allowed = cls._intersection(cls._not_allowed, data.keys())

        if len(missing_required) > 0 or len(included_not_allowed) > 0:
            raise InvalidFieldException(missing_required, included_not_allowed)
        
        return True

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


class ImplementationAncestorRapp(RappValidation):
    _required = ['display', 'description', 'public_interface', 'public_parameters', 'compatibility', 'launch']
    _optional = ['icon', 'pairing_clients', 'required_capability']
    _not_allowed = ['parent_specification']


class ImplementationChildRapp(RappValidation):
    _required = ['compatibility', 'launch', 'parent_specification']
    _optional = ['icon', 'pairing_clients', 'required_capability']
    _not_allowed = ['public_interface', 'public_parameters']
