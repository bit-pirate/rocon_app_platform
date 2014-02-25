#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_app_platform/license/LICENSE
#

##############################################################################
# Imports
##############################################################################

# enable some python3 compatibility options:
# (unicode_literals not compatible with python2 uuid module)
from __future__ import absolute_import, print_function

from nose.tools import assert_raises
import os
import rocon_console.console as console

from rocon_app_utilities.indexer import *
from rocon_app_utilities.rapp import *
from rocon_app_utilities.exceptions import *

##############################################################################
# Tests
##############################################################################

class TestRappIndexer():

    @classmethod
    def setup_class(cls):
        load_data(verbose=True)

    def setup(self):
        self.data = load_data()
        self.indexer = RappIndexer(self.data)

    def teardown(self):
        del self.data

    def test_inheritance(self): 
        console.pretty_println('Test Inherance', console.bold)


    def test_get_ancestor(self):
        console.pretty_println('Test Get Ancestor', console.bold)

    def test_get_nearest_parent(self):
        console.pretty_println('Test Get Nearest Parent', console.bold)

    def test_get_rapp(self):
        console.pretty_println('Test Get Rapp', console.bold)

    def test_get_complete_rapp(self):
        console.pretty_println('Test Get Complete Rapp', console.bold)
#        inherited_rapp = self.indexer.get_complete_rapp('basic/child')


def load_data(verbose=False):
    if verbose:
        console.pretty_println('Loading Test Rapps..',console.bold)
    pwd = os.getcwd() 
    data = {}
    data['basic/child'] = Rapp('basic/child', pwd + '/test_rapps/indexer/basic/child.rapp')
    data['basic/parent'] = Rapp('basic/parent', pwd + '/test_rapps/indexer/basic/parent.rapp')

    if verbose:
        for n in data:
            console.pretty_println(' - %s'% n)

    return data
