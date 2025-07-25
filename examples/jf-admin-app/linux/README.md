# Matter Joint Fabric Admin Example

An example application that acts as a Joint Fabric Administrator.

<hr>

-   [Matter Joint Fabric Admin Example](#matter-joint-fabric-admin-example)
    -   [Building the example Application on Linux](#building-the-example-application-on-linux)

<hr>

All the instructions given below assumes that we are in the connectedhomeip
repo, thus referencing the “top level”.

## Prepare for building

Before running any other build command, the `scripts/activate.sh` environment
setup script should be sourced at the top level. This script takes care of
downloading GN, ninja, and setting up a Python environment with libraries used
to build and test.

-   Run the following command at the top level:

          $ source scripts/activate.sh

## Checking if submodules are up to date

-   Pull the required submodules at the top level:

          $ ./scripts/checkout_submodules.py --shallow --platform linux

## Building the Example Application on Linux

-   Build the example application:

          $ cd examples/jf-admin-app/linux/
          $ gn gen out/debug
          $ ninja -C out/debug

-   To delete generated executable, libraries and object files use:

          $ cd examples/jf-admin-app/linux/
          $ rm -rf out/
