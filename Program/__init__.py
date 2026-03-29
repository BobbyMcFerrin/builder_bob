############################################################
# Program Init File
#
#
############################################################

import os, sys

GIT_BRANCH_NAME = "builder_bob"
FRAMEWORK_NAMESPACE = os.sep + GIT_BRANCH_NAME + os.sep
### Checking if inside NAMESPACE hierarchy
if __file__.find(FRAMEWORK_NAMESPACE) == -1:
    print("Program does not located inside {0} hierarchy"
          .format(FRAMEWORK_NAMESPACE))
    sys.exit(1)

base_directory = (__file__.split(FRAMEWORK_NAMESPACE)[0]
                  + FRAMEWORK_NAMESPACE)

sys.path.append(base_directory)
os.environ.setdefault('Bob', base_directory)
