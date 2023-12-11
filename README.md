usage: 
1. broadcast dummy data
TODO:

- [ ] actually get current data from car into protobuf encoded CAN messages and send them from current TCU / SAB

- [ ] get the raspberry pi listening to CAN messages

- [ ] adjust the foxglove server code host script to make it listen to CAN messages and switch between topics that it is sending based on the CAN IDs

- [ ] write the data storage script for saving the received CAN messages locally in the mcap 
    - [ ]  make service script that creates an instance of the mcap writer and the foxglove websocket
input: 
- protobuf stream (will be from CAN, this prototype will be from a port)

output: 
- saved files at time steps
- encoded websocket stream of data

- desired behavior for the data flow:
    - on hardware receive in the data_handler script data gets pushed into a container triggers both the webserver and the data writer to use that data
    - once both the data writer and the foxglove websocket have finished processing the data delete the data from the container

- I cant just used a single protobuf message that describes all of the data over CAN, I need to be able to differentiate between the different messages that come over the wire. 

- the thing needs to be able to differentiate between the different encoded message types and decode them accordingly.
- a desired workflow is that it all we need to do to add a new input that we will be seeing over the wire is to add a .proto to a specific folder. No code changes should be required.
- i know that an any protobuf data type can kinda handle these types of requirements


notes:
- filter journalctl based on service: `journalctl -u nginx.service`
