"""
test main
may become integration test
"""
# Date:         12 Aug 2023
# Revision History:
#	resultay | 12-08-23 | Force load

from sample import main

# since no games are implemented yet
# there is no reason to test anything
def test_nothing():
    """function opens menu"""
    assert main()
