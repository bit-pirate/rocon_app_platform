#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_app_platform/license/LICENSE
#
#################################################################################

from __future__ import division, print_function 

import sys
import os
import traceback

from yujin_tools import console
import rocon_utilities
from .utils import *
from .params import MAX_CACHE_AGE
from .rapp import Rapp, MetaRapp

#################################################################################
# Global method
#################################################################################

def update_cache():
    '''
        Retrieve rapps in ROS_PACKAGE_PATH, resolve all nested rapp specification,
        and update the cache
    '''
    cache_path = get_cache_path()
    rapp_path = load_rapp_path_dict()

    for name, path in rapp_path.items():
        print(name + " : " + path)


    # TODO
    # for each rapp
    #   validate if any attribute is missing.
    #   if it misses, resolve them with parent specification chain
    #   if it does not meet all required attributes, don't add into cache
    # update the cache age

    # Load rapp from file. After this rapp dictionary should contain only valid rapps 
    # invalid_rapps will be resolved with parent specification
    """
    rapp, invalid_rapp = _load_specs_from_file(rapp_path, Rapp)
    meta_rapp, invalid_meta_rapp = _load_specs_from_file(metarapp_path, MetaRapp)

    parent_index = _create_parent_index(rapp, meta_rapp, invalid_rapp)
    rapp_index = dict(rapp, **meta_rapp)

    # Lets resolve invalid rapps with parent specification
    for name, inval_rapp in invalid_rapp.items():
        parent_name = parent_index[name]
        if not parent_name:
            console.warning('[' + name + '] misses required attribute ' + str(inval_rapp.validate()) + ' and does not have parent specification')

        parent = rapp_index[parent_name]

        # the root parent must be in the valid rapp_index
    """





    pass


def validate_cache():
    '''
        Check when cache get updated and 
    '''
    # TODO
    user_cache_timeout = os.getenv('ROS_CACHE_TIMEOUT')
    return True


#################################################################################
# local methods 
#################################################################################


def _load_specs_from_file(rapp_path, RappObject):
    '''
        load rapp or meta rapp from file and return rapp dict and invalid rapp dict

        @return valid dict and invalid dict
        @rtype {name:RappObject}, {name: (RappObject, missing dependency)}
    '''
    rapp = {}
    invalid_rapp = {}
    for name, path in rapp_path.items():
        r = RappObject()
        missing_required_attributes = r.load_from_file(path)
        if not missing_required_attributes:
            rapp[name] = r
        else:
            invalid_rapp[name] = r 

    return rapp, invalid_rapp

def _create_parent_index(rapp, meta_rapp, invalid_rapp):
    # TODO: We might want to create rapp parent tree to optimize rapp resolution

    parent_index = {}
    # Put all of them into one dictionary with its parent name. If parent is None, it is the root
    _add_parent(parent_index, rapp)
    _add_parent(parent_index, meta_rapp)
    _add_parent(parent_index, invalid_rapp)

    # for each rapp search for the root parent
    for name in parent_index:
        parent_index[name] = _search_root_parent(name, parent_index)

    return parent_index

def _search_root_parent(name, parent_index):
    '''
        Traverse parent index dictionary to get root parent of rapp

        @param rapp name
        @type str 
        @param parent name indexed dictionary 
        @type dict

        @return root parent rapp name. returns None if it is root
        @rtype str
    '''
    current_name = name
    prev_name = current_name
    while current_name in parent_index:
        prev_name = current_name
        current_name = parent_index[current_name]

    if prev_name == name:
        return None
    else:
        return prev_name 


def _add_parent(parent_index, rapp):
    for name, r in rapp.items():
        if name in parent_index:
            console.warning('[' + name + '] exist already in parent index!')
        parent_index[name] = r.get_parent()
