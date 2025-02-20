from axi4_agent import AXI4Bundle, AXI4MasterAgent
from UT_AXI4RAM import DUTAXI4RAM
from toffee import *

class AXI4Model(Model):
    def __init__(self):
        super().__init__()
        self.mem = {}

#在参考模型中，我们同样定义了一个 exec_add 方法，该方法与 Agent 中的 exec_add 方法含有相同的输入参数，我们用程序代码计算出了加法器的标准返回值#。我们使用了 driver_hook 装饰器来标记该方法，以便该方法可以与 Agent 中的 exec_add 方法进行关联。#
#toffee 会自动驱动参考模型并收集结果，并将结果与加法器的输出进行比对#
    @driver_hook(agent_name="in_agent")
    def read(self, addr, len):
        result = [self.mem.get((addr >> 3) + i, 0) for i in range(len)]
        with open ('/home/haom/work/xs/xs-mlvp-demo1/toffee-cases/axi4/toffee/test_out.txt','a') as f:
            print("modle result = ",file=f)
            print(self.mem.get((addr >> 3) + 0, 0))
        return result

    @driver_hook(agent_name="in_agent")
    def write(self, addr, data):
        for i, d in enumerate(data):
            self.mem[(addr >> 3) + i] = d
        return 0

class AXI4Env(Env):
    def __init__(self, dut:DUTAXI4RAM):
        super().__init__()
        axi4_bundle = AXI4Bundle.from_prefix("io_in_").bind(dut)
        self.in_agent = AXI4MasterAgent(axi4_bundle)
        self.attach(AXI4Model())
        self.dut = dut
        #self.dut.InitClock("clock")

        # Reset
        self.reset()

    def reset(self):
        self.dut.reset.value = 1
        self.dut.Step(1)
        self.dut.reset.value = 0
        self.dut.Step(1)