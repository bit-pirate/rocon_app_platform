#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_app_platform/license/LICENSE
#
#################################################################################

from __future__ import division, print_function 

#################################################################################
# Imports
#################################################################################

import os
import sys
import traceback
import argparse
import rocon_uri

#################################################################################
# Global 
#################################################################################

class RappTemplate(object):

    def __init__(self, name, display=None,description=None, compatibility=None, parent=None):
        data = {}
        data['name'] = name
        data['display'] = display if display else name
        data['description'] = description if description else ''
        data['compatibility'] = rocon_uri.RoconURI(compatibility) if compatibility else rocon_uri.RoconURI()

        # We might want to validate the value later
        data['parent'] = parent

        self.data = data
    

def parse_arguments(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Creates a new Rapp')
    parser.add_argument('NAME', help='The name for the rapp')
    parser.add_argument('--display', action='store',help='Rapp display name')
    parser.add_argument('--description', action='store',help='Description')
    parser.add_argument('--compatibility', action='store',help='Rapp display name')
    parser.add_argument('--parent', action='store',help='Parent Specification')
    args = parser.parse_args(argv)
    return args


def create_rapp_files(name, target_path, rapp_template):
    # Create
    if not os.path.exist(target_path):
        os.mkdir(target_path)

    # TODO ....It requires too much effort than I expected.. reference instantiate_template function in init_build.py in yujin_tools for further implementation later.
    pass



def main():
    args = parse_arguments()
    parent_path = os.getcwd()
    
    try:
        rapp_name = args.NAME
        target_path = os.path.join(parent_path, rapp_name)
        rapp_template = RappTemplate(name=rapp_name, display=args.display, description=args.description, compatibility=args.compatibility, parent=args.parent)

        create_rapp_files(rapp_name, target_path, rapp_template)
        print('Successfully created rapps in %s.\nPlease adjust the values in rapp.' % target_path)
        
    except Exception as e:
        print('Rocon Create App Error : ' + str(e))
        ex_type, ex, tb = sys.exc_info()
        traceback.print_tb(tb)
