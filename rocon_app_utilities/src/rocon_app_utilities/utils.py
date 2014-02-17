#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_app_platform/license/LICENSE
#
#################################################################################

from __future__ import division, print_function 

import os
import rocon_utilities
from yujin_tools import console
from rocon_app_manager.rapp import Rapp
from .params import DOTROS_NAME, RAPP_PATH

#################################################################################
# global methods 
#################################################################################

def get_cache_path():
    '''
      Get a place to store cache. It looks up for $ROS_HOME. If it does not exist, it stores in DOTROS_NAME under home directory
    '''
    cache_path = _find_cache_rootpath()

    # If the cache path does not exist create one.
    if not os.path.exists(cache_path):
            os.mkdir(cache_path)
    return cache_path


def _find_cache_rootpath():
    '''
       Resolves the path to store rapp cache
    '''
    cache_path = ''
    ros_home = os.getenv('ROS_HOME')
    if ros_home:
        cache_path = ros_home
    else:
        # TODO Window support just as rospack does. It only support UNIX for now
        home_path = os.getenv('HOME')
        if home_path:
            cache_path = os.path.join(home_path, DOTROS_NAME)
    cache_path = os.path.join(cache_path, RAPP_PATH)

    return cache_path
    

def load_rapp_path_dict(): 
    '''
      Retrieves rapps found in the package path. 

      @return rapp dictionary, meta rapp dictionary 
      @rtype {'rapp_uniquename':'its absolute path'}
    '''
    rapp = {}
    meta_rapp = {}
    package_index = get_package_index()
    for package in package_index.values():
        for export in package.exports:
            if export.tagname == 'rocon_app':
                rapp_name, rapp_path = _get_rapp_path(package, export.content)
                if rapp_name in rapp:
                    console.warning('Warning! Rapp [' + rapp_name + '] already exist. overwriting the existing one..')
                rapp[rapp_name] = rapp_path
            elif export.tagname == 'rocon_metaapp':
                rapp_name, rapp_path = _get_rapp_path(package, export.content)
                if rapp_name in meta_rapp:
                    console.warning('Warning! Rapp [' + rapp_name + '] already exist. overwriting the existing one..')
                meta_rapp[rapp_name] = rapp_path

    return rapp, meta_rapp


def _get_rapp_path(package, package_relative_rapp_filename): 
    '''
      Parse package information and return rapp unique name and its absolute path 

      @param package this rapp is nested in
      @type :py:class:`catkin_pkg.package.Package`
      @param package_relative_rapp_filename : string specified by the package export
      @type os.path

      @return rapp unique name
      @rtype str
      @return rapp absolute path
      @rtype os.path
    '''
    package_path = os.path.dirname(package.filename)
    rapp_path = os.path.join(package_path, package_relative_rapp_filename)
    rapp_name = package.name + '/' + os.path.splitext(os.path.basename(rapp_path))[0]
      
    return rapp_name, rapp_path
    

def get_package_index():
    ros_package_path = os.getenv('ROS_PACKAGE_PATH', '')
    ros_package_path = [x for x in ros_package_path.split(':') if x]
    package_index = rocon_utilities.package_index_from_package_path(ros_package_path)
    return package_index
