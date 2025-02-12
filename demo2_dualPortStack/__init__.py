#from src.test.test_example import *
from src.test.test_example_async import *

ASYNC = True

if __name__ == "__main__":
    dut = DUTdual_port_stack()
    dut.InitClock("clk")
    if(ASYNC):
        asyncio.run(test_stack(dut))
    else:
        test_stack(dut)
    dut.Finish()
 
  
#    dut = DUTdual_port_stack()
#    dut.InitClock("clk")
#    asyncio.run(test_stack(dut))
#    dut.Finish()
