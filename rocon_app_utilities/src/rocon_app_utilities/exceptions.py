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


class InvalidRappException(RappException):
    '''
        Invalid format of rapp
    '''
    pass

class ParentRappNotFoundException(RappException):
    '''
        Parent Not Found Exception
    '''
    pass

class RappInvalidChainException(RappException):
    '''
        If the rapp chain is invalid.
    '''
    pass


class RappNotExistException(RappException):
    '''
        When Rapp does not exist 
    '''
    pass


class InvalidRappFieldException(RappException):
    '''
        It does not satisfy required or not allowed field
    '''
    def __init__(self, invalid_required, invalid_not_allowed):
        self.invalid_required = invalid_required
        self.invalid_not_allowed = invalid_not_allowed

    def __str__(self):
        return str('\n\tMissing Requirements - ' + str(self.invalid_required) + '\n\tInvalid Not Allowed - ' + str(self.invalid_not_allowed))
