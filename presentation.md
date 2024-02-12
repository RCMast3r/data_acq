## a new approach to data acquisition 

- intro about what the goal of data acquistion is
    - live data viewing
    - "run to run" data recording
    - long-term data storage and ease of access to previous recordings
    - car performance over time

- an introduction to CAN and DBC files
    - CAN is the largest source of data on the car
        - most of the boards connect over CAN for board-to-board comms and telemetry readouts
    - CAN is a serialized protocol which requires both serialization to encode data and move it accross the wire and deserialization for receiving data from the wire and getting it into a usable format or struct. 
    - The standard way of handling this process is through DBC files.
    - https://www.csselectronics.com/pages/can-dbc-file-database-intro
    - DBC files can be used by numerous tools for analysis and automatic deserialization of CAN traffic via libraries like `cantools` or any of the other tools lists here:
    https://github.com/iDoka/awesome-canbus?tab=readme-ov-file#converters-and-parsers
    - DBC files are most often uses for generation of C libraries for handling of the monotenous task of creating deserialization and serialization at the micro-controller level
    - formats similar to DBC that do the same thing
        - `.sym` files

- generation of libraries from DBC files
    - hytech's initial DBC file has already been put together and is ready for use!
    - several workflows exist for handling generation and use of the low-level generated serialization and deserialization library
    - CI generated HT_CAN library 
    - the platformio add in for local library generation

- what else do you do with these dbc files?
    - so far we have only covered the low-level handling of the CAN interface
    - single board computer for dbc based parsing of CAN network
    - CAN works well as a protocol over the wire because of it's ability to elegantly handle prioritization of messages and overcome noise issues however we have better protocols at the high level for internet based communication
    - we can use the DBC file to create the higher level communication protocol definitions
        - simple methods for meta analysis of the DBC definition

- what is protobuf?
    - protobuf solves the same problem as DBC files do for the low level but is designed to be used with internet based protocols or streams
    - at it's core it is based around `.proto` files and these files are used with a native tool called `protoc` for creating serialization and deserialization libraries for most any language
    - nix integration and automation
        - Tim Gallion's nix wrapper for `protoc` for automated package management and vertically integrated stacks:
            - https://github.com/notalltim/nix-proto 

- generation of protobuf message schemas leveraging cantools
    - we can use DBC files to create these proto files via a simple python script which has been implemented here:
        - https://github.com/RCMast3r/data_acq/blob/master/py_dbc_proto_gen/dbc_to_proto.py

- foxglove studio (live view)

- mcap files (run to run data reccording)
    - comparison to database approaches

- ease of deployment and automation
    - the role of nix and nixos

- the workflow as a whole at the birds-eye view

- the end result and the proposed pipeline

- solving the big evolving data problem

- how do I get involved?
    - list of the github projects that are involved
    - beginner issues lists
