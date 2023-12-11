# this thingy will handle the receiving of the CAN data over hardware and 
# provide it to whatever needs it.

import asyncio

# I think what I want is that this thing is given some asyncio object that will serve as the data pipeline into the 2 services in the data writer service.
# this way, the hardware that is actually receiving the data can easily be switched out and between.

