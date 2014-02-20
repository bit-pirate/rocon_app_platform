#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_app_platform/license/LICENSE
#
#################################################################################

from __future__ import division, print_function 

from .rapp import Rapp, MetaRapp

from .params import DEFAULT_ROCON_URI

class RappIndexer(object):

    def __init__(self):
        self.raw_data = {}

        # TODO : We might want to manipulate raw_data to have better format in the future. e.g) cache creation
        # self.data = {} 
        pass

    def get_parent(self, rapp_name):
        '''
          returns given rapps one level above parent
        '''
        # TODO : 
        pass

    def get_root_parent(self, rapp_name):
        '''
          returns the root parent Rapp Instance of given name
        '''
        pass

    def get_rapp(self, rapp_name):
        '''
          returns Rapp Instance of given name
        '''
        pass

    def get_compatible_rapps(self, rocon_uri=DEFAULT_ROCON_URI): # TODO: add capability check later
        '''
          returns all rapps which are compatible with given URI 
        '''
        pass

    def to_dot(self):
        '''
            returns the dot graph format
        '''
        # TODO
        pass
