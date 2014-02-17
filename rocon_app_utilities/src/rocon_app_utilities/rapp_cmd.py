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
import argparse


import rocon_utilities
import rapp_profiler 

#################################################################################
# Global variables
#################################################################################

NAME='rapp'

#################################################################################
# global methods 
#################################################################################

#################################################################################
# Local methods 
#################################################################################

def _rapp_cmd_list(argv):
    """
      Command-line parsing for 'rapp list' command.
    """

    # Parse command arguments
    args = argv[2:]
    parser = argparse.ArgumentParser(description='Displays list of rapps')
    list_group = parser.add_mutually_exclusive_group()
    list_group.add_argument('-b','--black-list', default=[], help='Specify package black list')
    list_group.add_argument('-w','--white-list', default=[], help='Specify package white list')
    parsed_args = parser.parse_args(args)

    # Converting [rocon_apps,turtle_concert] comma seperated string into list
    if parsed_args.white_list:
        parsed_args.white_list = parsed_args.white_list[1:-1].split(',')
    if parsed_args.black_list:
        parsed_args.black_list = parsed_args.black_list[1:-1].split(',')


def _rapp_cmd_info(argv):
    print("Displays rapp information")
    pass


def _rapp_cmd_depends(argv):
    print("Dependecies")
    pass


def _rapp_cmd_depends_on(argv):
    print("Childs")
    pass

def _rapp_cmd_profile(argv):
    rapp_profiler.update_cache()
    pass

def _rapp_cmd_compat(argv):
    print("Compat")
    pass

def _fullusage():
    print("""\nrapp is a command-line tool for printing information about Rapp

Commands:
\trapp list\tdisplay a list of cached rapps
\trapp info\tdisplay rapp information
\trapp depends\tdisplay a rapp dependency list
\trapp depends-on\tdisplay a list of rapps that depend on the given rapp
\trapp profile\tupdate cache
\trapp compat\tdisplay a list of rapps that are compatible with the given rocon uri
\trapp help\tUsage

Type rapp <command> -h for more detailed usage, e.g. 'rapp info -h'
""")
    sys.exit(getattr(os,'EX_USAGE',1))


#################################################################################
# Main  
#################################################################################

def main():
    argv = sys.argv

    # process argv
    if len(argv) == 1:
        _fullusage()
    try:
        command = argv[1]
        if command == 'list':
            _rapp_cmd_list(argv) 
        elif command == 'info':
            _rapp_cmd_info(argv)
        elif command == 'depends':
            _rapp_cmd_depends(argv)
        elif command == 'depends-on':
            _rapp_cmd_depends_on(argv)
        elif command == 'profile':
            _rapp_cmd_profile(argv)
        elif command == 'compat':
            _rapp_cmd_compat(argv)
        elif command == 'help':
            _fullusage()
        else:
            _fullusage()
    except Exception as e:
        sys.stderr.write("Error: %s\n"%str(e))
        ex, val, tb = sys.exc_info()
        traceback.print_exception(ex, val, tb)

        sys.exit(1)
