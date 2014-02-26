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

from nose.tools import assert_raises, assert_true
import os
import rocon_console.console as console

from rocon_app_utilities.rapp import *
from rocon_app_utilities.exceptions import *

##############################################################################
# Tests
##############################################################################

pwd = os.getcwd() 

def test_rapp_loading(): 
    print(console.bold + "\n****************************************************************************************" + console.reset)
    print(console.bold + "* Raising on Invalid Rapp Loading" + console.reset)
    print(console.bold + "****************************************************************************************" + console.reset)

    console.pretty_println('Extra Field', console.bold)
    filename = pwd + '/test_rapps/rapp/invalid_loading/invalid_attribute.rapp'
    console.pretty_println(' - %s'% filename)
    assert_raises(InvalidRappException, load_rapp_from_file, filename)

    # console.pretty_println('Duplicated Field',console.bold)
    # TODO

def test_rapp_classification():
    def test_one(Except, func, filename):
        f = pwd + filename
        data = load_rapp_from_file(f)
        console.pretty_println(' - %s'%f)
        assert_raises(Except, classify_rapp_type, data)

    print(console.bold + "\n****************************************************************************************" + console.reset)
    print(console.bold + "* Raising on Invalid Rapp Classification" + console.reset)
    print(console.bold + "****************************************************************************************" + console.reset)

    console.pretty_println('Virtual Child', console.bold)
    test_one(InvalidRappException,      classify_rapp_type, '/test_rapps/rapp/invalid_classification/virtual_child1.rapp')
    test_one(InvalidRappException,      classify_rapp_type, '/test_rapps/rapp/invalid_classification/virtual_child2.rapp')

    console.pretty_println('Invalid Virtual Ancestor', console.bold)
    test_one(InvalidRappFieldException, classify_rapp_type, '/test_rapps/rapp/invalid_classification/invalid_virtual_ancestor1.rapp')
    test_one(InvalidRappFieldException, classify_rapp_type, '/test_rapps/rapp/invalid_classification/invalid_virtual_ancestor2.rapp')
    test_one(InvalidRappFieldException, classify_rapp_type, '/test_rapps/rapp/invalid_classification/invalid_virtual_ancestor3.rapp')

    console.pretty_println('Invalid Implementation Ancestor', console.bold)
    test_one(InvalidRappFieldException, classify_rapp_type, '/test_rapps/rapp/invalid_classification/invalid_implementation_ancestor1.rapp')
    test_one(InvalidRappFieldException, classify_rapp_type, '/test_rapps/rapp/invalid_classification/invalid_implementation_ancestor2.rapp')
    test_one(InvalidRappFieldException, classify_rapp_type, '/test_rapps/rapp/invalid_classification/invalid_implementation_ancestor3.rapp')
    test_one(InvalidRappFieldException, classify_rapp_type, '/test_rapps/rapp/invalid_classification/invalid_implementation_ancestor4.rapp')
    test_one(InvalidRappFieldException, classify_rapp_type, '/test_rapps/rapp/invalid_classification/invalid_implementation_ancestor5.rapp')

    console.pretty_println('Invalid Implementation Child', console.bold)
    test_one(InvalidRappFieldException, classify_rapp_type, '/test_rapps/rapp/invalid_classification/invalid_implementation_child1.rapp')

    console.pretty_println('Field Confilct Rapp', console.bold)
    test_one(InvalidRappFieldException, classify_rapp_type, '/test_rapps/rapp/invalid_classification/conflict.rapp')

def test_rapp_field_validation():
    # TODO
    pass

def test_rapp_inheritance():
    def inherit_pair(path):
        filename = pwd + path + '/child.rapp'
        child = Rapp('child',filename) 
        filename = pwd + path + '/parent.rapp'
        parent = Rapp('parent',filename) 

        child.inherit(parent)
        return child

    def validate(data, valid_data): 
        for f, d in valid_data:
            if not f in data: 
                return False
            if not data[f] == d:
                return False

        return True

    print(console.bold + "\n****************************************************************************************" + console.reset)
    print(console.bold + "* Rapp Inheritance" + console.reset)
    print(console.bold + "****************************************************************************************" + console.reset)

    # full inheritance
    path = '/test_rapps/rapp/inherity/full'
    console.pretty_println(' - %s'%path) 
    child = inherit_pair(path)

    d = [('display',           'Talker'),
         ('description',       'Default ros style talker tutorial'),
         ('public_interface',  'rocon_apps/talker.interface'),
         ('public_parameters', 'rocon_apps/talker.parameters'),
         ('icon',              'rocon_apps/talker.png')]
    assert_true(validate(child.data, d))
    

    # icon and publics
    path = '/test_rapps/rapp/inherity/icon_and_publics'
    console.pretty_println(' - %s'%path) 
    child = inherit_pair(path)
    d = [('display',           'Child Talker in icon and publics'),
         ('description',       'Hola Child...........'),
         ('public_interface',  'rocon_apps/talker.interface'),
         ('public_parameters', 'rocon_apps/talker.parameters'),
         ('icon',              'rocon_apps/talker.png')]
    assert_true(validate(child.data, d))

    # publics
    path = '/test_rapps/rapp/inherity/publics'
    console.pretty_println(' - %s'%path) 
    child = inherit_pair(path)
    d = [('display',           'Child Talker in publics'),
         ('description',       'public public child'),
         ('public_interface',  'rocon_apps/talker.interface'),
         ('public_parameters', 'rocon_apps/talker.parameters')]
    assert_true(validate(child.data, d))

    # from meta
    path ='/test_rapps/rapp/inherity/from_meta'
    console.pretty_println(' - %s'%path) 
    child = inherit_pair(path)
    d = [('display',           'Talker in from meta'),
         ('description',       'from meta meta meta metaaaaaaaaa'),
         ('public_interface',  'rocon_apps/talker.interface'),
         ('public_parameters', 'rocon_apps/talker.parameters'),
         ('icon',              'rocon_apps/talker.png')]
    assert_true(validate(child.data, d))


    # from another child
    path = '/test_rapps/rapp/inherity/from_child'
    console.pretty_println(' - %s'%path) 
    child = inherit_pair(path)
    d = [('display',           'Talker'),
         ('description',       'Default ros style talker tutorial'),
         ('icon',              'rocon_apps/talker.png')]
    assert_true(validate(child.data, d))
