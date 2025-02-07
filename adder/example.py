try:
    from UT_adder import *
except:
    try:
        from adder import *
    except:
        from __init__ import *


if __name__ == "__main__":
    dut = DUTadder()
    # dut.init_clock("clk")

    dut.Step(1)

    dut.Finish()
