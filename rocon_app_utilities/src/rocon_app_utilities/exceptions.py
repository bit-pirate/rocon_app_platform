#!/usr/bin/env python
#
# License: BSD
#   https://raw.github.com/robotics-in-concert/rocon_app_platform/license/LICENSE
#
#################################################################################

class RappException(Exception):
    """
        Rapp Exception
    """
    pass

class ParentNotFoundException(RappException):
    """
        Parent Not Found Exception
    """
    pass

