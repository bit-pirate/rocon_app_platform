#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_app_platform/license/LICENSE
#
#################################################################################

from __future__ import division, print_function 
import yaml

from .exceptions import *

IMPLEMETATION_VALIDATION_LIST = ['launch', 'compatibility']
CHILD_VALIDATION_LIST = ['parent_specification']
RAPP_ATTRIBUTES = ['display', 'description', 'icon', 'public_interface', 'public_parameters', 'compatibility', 'launch', 'parent_specification', 'pairing_clients', 'required_capability']
INHERITABLE_ATTRIBUTES = ['display', 'description', 'icon', 'public_interface', 'public_parameters', 'parent_specification']

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


def load_rapp_from_file(filename):
    '''
        Load rapp specs from the given file
    '''
    with open(filename, 'r') as f:
        app_data = yaml.load(f.read())

        for d in app_data:
            if d not in RAPP_ATTRIBUTES:
                raise InvalidRappException('Invalid Field : ' + str(d))

    return app_data


def classify_rapp_type(data):
    '''
        Classify the current rapp among VirtualAncestor, ImplementationAnacestor, ImplementationChild 
    '''
    is_impl = _is_implementation_rapp(data)
    is_ance = _is_ancestor_rapp(data)

    impl = 'Implementation' if is_impl else 'Virtual'
    ance = 'Ancestor' if is_ance else 'Child'
    try:
        if is_impl and is_ance: # Implementation Ancestor
            ImplementationAncestorRapp.is_valid(data)
        elif is_impl and not is_ance: # Implementation Child
            ImplementationChildRapp.is_valid(data)
        elif not is_impl and is_ance: # Virtual Ancestor
            VirtualAncestorRapp.is_valid(data)
        else:                         # Virtual Child
            raise InvalidRappException('Virtual Child rapp. Invalid!')
    except InvalidRappFieldException as ife:
        raise ife
        
    t = str(impl + ' ' + ance)
    return is_impl, is_ance, t 


def validate_rapp_field(data):
    '''
        Validate each field. E.g) check rocon uri. Check the linked file exist 
    '''
    #  TODO
    pass


class Rapp(object):


    def __init__(self, name, filename=None):
        self.name = name
        self.data = {}
        self.type = None

        if filename: 
            self.load_from_file(filename)
            #validate_rapp_field(self.dat)
            self.classify()


    def __str__(self):
        return str(self.name)

    def classify(self):
        self.is_impl, self.is_ance, self.type = classify_rapp_type(self.data)

    def load_from_file(self, filename):
        self.data = load_rapp_from_file(filename)
        self.classify()


    def get_parent(self):
        '''
            @return Returns parent rapp name
            @rtype str 
        '''
        return self.data['parent_specification'] if 'parent_specification' in  self.data else None


    def inherit(self, rapp):
        '''
            Inherits missing information from the given rapp
        '''

        # Once it inherits, it removes parent_specification field. If it is inherits from another child, it obtains parent_specification anyway
        del self.data['parent_specification']

        for attribute in INHERITABLE_ATTRIBUTES:
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
            raise InvalidRappFieldException(cls, missing_required, included_not_allowed)
        
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
    _required = ['display', 'description']
    _optional = ['icon', 'public_interface', 'public_parameters']
    _not_allowed = ['compatibility', 'launch', 'parent_specification', 'pairing_clients', 'required_capability']


class ImplementationAncestorRapp(RappValidation):
    _required = ['display', 'description', 'compatibility', 'launch']
    _optional = ['icon', 'pairing_clients', 'required_capability', 'public_interface', 'public_parameters']
    _not_allowed = ['parent_specification']


class ImplementationChildRapp(RappValidation):
    _required = ['compatibility', 'launch', 'parent_specification']
    _optional = ['icon', 'pairing_clients', 'required_capability']
    _not_allowed = ['public_interface', 'public_parameters']
