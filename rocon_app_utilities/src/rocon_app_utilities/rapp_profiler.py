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
    rapp_path, metarapp_path = load_rapp_path_dict()

    # TODO
    # for each rapp
    #   validate if any attribute is missing.
    #   if it misses, resolve them with parent specification chain
    #   if it does not meet all required attributes, don't add into cache
    # update the cache age

    # Load rapp from file. After this rapp dictionary should contain only valid rapps 
    # invalid_rapps will be resolved with parent specification

    rapp, invalid_rapp = _load_specs_from_file(rapp_path, Rapp)
    meta_rapp, invalid_meta_rapp = _load_specs_from_file(metarapp_path, MetaRapp)

    # TODO: We might want to create rapp parent tree to optimize rapp resolution

    # Lets resolve invalid rapps with parent specification
    print('Invalid Apps')
    for name, r in invalid_rapp.items():
        _, missing = r
        print(name + ' : ' + str(missing))

    print('Valid Rapp')
    for name in rapp:
        print(name)
    print('Valid Meta Rapp')
    for name in meta_rapp:
        print(name)

    print('InValid Meta Rapp')
    for name, r in invalid_meta_rapp.items():
        _, missing = r
        print(name + ' : ' + str(missing))
    
    """
    for name, inval_rapp in invalid_rapp.itimes():
        r, missing_attribute = invalid_rapp
        parent = r.get_parent()

        if not parent: 
            console.warning('[' + name + '] misses required attribute ' + str(missing_attribute) + ' and does not have parent specification')
        else:
            root_parent = _search_root_parent(parent)
    pass
    """



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
            invalid_rapp[name] = (r, missing_required_attributes)

    return rapp, invalid_rapp
