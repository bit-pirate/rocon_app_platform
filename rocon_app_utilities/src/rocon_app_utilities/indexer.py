#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_app_platform/license/LICENSE
#
#################################################################################

from __future__ import division, print_function 
import copy

#from .rapp import Rapp, MetaRapp
from .utils import load_rapp_path_dict
from .params import DEFAULT_ROCON_URI
from .exceptions import *
from .rapp import Rapp
from rocon_console import console

class RappIndexer(object):

    def __init__(self):
        self.raw_data_path = {}
        self.raw_data = {}

        # TODO : We might want to manipulate raw_data to have better format in the future. e.g) cache creation
        # self.data = {} 

        self.update_index()

        pass

    def update_index(self):
        '''
            Crawls rocon apps from ROS_PACKAGE_PATH and generates raw_data dictionary
        '''
        self.raw_data_path = load_rapp_path_dict()

        raw_data = {}

        console.pretty_println('Crawling ROS_PACKAGE_PATH...',console.bold)
        for name, path in self.raw_data_path.items():
            try:
                r = Rapp(name)
                r.load_from_file(path)
                r.classify()
                raw_data[name] = r
                console.pretty_println('  [' + name + '] : ' + str(r.type) + ' has been added')
            except InvalidRappFieldException as irfe:
                console.warning('  [' + name + '] has not been added : ' + str(irfe))
            except InvalidRappException as ire:
                console.warning('  [' + name + '] has not been added : ' + str(ire))
            except Exception as e:
                console.warning('  [' + name + '] has not been added :' + str(e))


        console.pretty_println('Available Rapps',console.bold)
        for name, rapp in raw_data.items():
            print('  ' + str(name) + ' : ' + str(rapp.type))


    def get_nearest_parent(self, rapp_name):
        '''
          returns the nearest parent instance of the given rapp

          @param rapp_name
          @type str

          @return parent rapp name if it does not have it return None
          @rtype str
        '''
        if not rapp_name in self.raw_data:
            raise RappNotExistException(str(rapp_name) + ' does not exist')

        return self.raw_data[rapp_name].get_parent()

    def get_ancestor(self, rapp_name):
        '''
          @return the acestor rapp name of given rapp
          @rtype str
        '''
        if not rapp_name in self.raw_data:
            raise RappNotExistException(str(rapp_name) + ' does not exist')

        current_rapp = rapp_name
        while not self.raw_data[current_rapp].is_ancestor():
            current_rapp = self.raw_data[current_rapp].get_parent()

        return current_rapp

    def get_rapp(self, rapp_name):
        '''
          returns rapp instance of given name
        '''
        if not rapp_name in self.raw_data:
            raise RappNotExistException(str(rapp_name) + ' does not exist')

        return self.raw_data[rapp_name]

    def get_complete_rapp(self, rapp_name):
        '''
          returns complete rapp instance which includes inherited attributes from its parent

          @param rapp name
          @type str

          @return rapp instance
          @rtype rocon_app_utilities.rapp.Rapp
        '''
        if not rapp_name in self.raw_data:
            raise RappNotExistException(str(rapp_name) + ' does not exist')

        rapp = self._resolve(rapp_name)

        return rapp

    def get_compatible_rapps(self, rocon_uri=DEFAULT_ROCON_URI): # TODO: add capability check later
        '''
          returns all rapps which are compatible with given URI 
        '''
        # TODO
        pass

    def _resolve(self, rapp_name):
        '''
            resolve the rapp instance with its parent specification and return a runnable rapp
        '''
        rapp = copy.deepcopy(self.raw_data[rapp_name]) # Not to currupt original data
        parent = rapp.get_parent()
        
        return self._resolve_recursive(rapp, parent)

    def _resolve_recursive(self, rapp, parent_name):
        '''
            Internal method of _resolve
        '''

        if rapp.is_ancestor():
            return rapp

        if not parent_name:
            raise RappInvalidChainException('Invalid Rapp Chain from [' + str(rapp)+']')

        if not parent_name in self.raw_data:
            raise ParentRappNotFoundException(parent_name)

        parent = self.raw_data[parent_name]
        rapp.inherit(parent)

        return self._resolve_recursive(rapp, parent.get_parent())


    def to_dot(self):
        '''
            returns the dot graph format
        '''
        # TODO
        pass
