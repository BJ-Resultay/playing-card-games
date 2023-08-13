# Date:         12 Aug 2023
# Description:  Test main
#               This may become an integration test instead
# Revision History:
#	resultay | 12-08-23 | Force load

from sample import main

# since no games are implemented yet
# there is no reason to test anything
def test_nothing():
    assert main.main()
