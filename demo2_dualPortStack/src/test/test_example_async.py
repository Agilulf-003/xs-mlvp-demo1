import asyncio
import random
from dual_port_stack import *
from enum import Enum

class StackModel:
    def __init__(self):
        self.stack = []

    def commit_push(self, data):
        self.stack.append(data)
        print("Push", data)

    def commit_pop(self, dut_data):
        print("Pop", dut_data)
        model_data = self.stack.pop()
        assert model_data == dut_data, f"The model data {model_data} is not equal to the dut data {dut_data}"
        print(f"Pass: {model_data} == {dut_data}")

class SinglePortDriver:
    class BusCMD(Enum):
        PUSH = 0
        POP = 1
        PUSH_OKAY = 2
        POP_OKAY = 3

    def __init__(self, dut, model: StackModel, port_dict):
        self.dut = dut
        self.model = model
        self.port_dict = port_dict

    async def send_req(self, is_push):
        self.port_dict["in_valid"].value = 1
        self.port_dict["in_cmd"].value = self.BusCMD.PUSH.value if is_push else self.BusCMD.POP.value
        self.port_dict["in_data"].value = random.randint(0, 2**8-1)
        await self.dut.AStep(1)

        await self.dut.Acondition(lambda: self.port_dict["in_ready"].value == 1)
        self.port_dict["in_valid"].value = 0

        if is_push:
            self.model.commit_push(self.port_dict["in_data"].value)

#await 是 Python 的 asyncio 库中用于异步编程的关键字。
#当你在协程函数（使用 async def 定义的函数）内部遇到耗时操作，
#如 I/O 操作、网络请求等，可以使用 await 来暂停该协程的执行，直到等待的操作完成。
#这允许其他协程在此期间运行，从而提高程序的整体效率和响应性。

    async def receive_resp(self):
        self.port_dict["out_ready"].value = 1
        await self.dut.AStep(1) # driver wait dut 
#async AStep(cycle: int)      #异步推进cycle个时钟， eg：await dut.AStep(5)
#async ACondition(condition)  #异步等待conditon()为true
        await self.dut.Acondition(lambda: self.port_dict["out_valid"].value == 1)
        self.port_dict["out_ready"].value = 0

        if self.port_dict["out_cmd"].value == self.BusCMD.POP_OKAY.value:
            self.model.commit_pop(self.port_dict["out_data"].value)

    async def exec_once(self, is_push):
        await self.send_req(is_push)
        await self.receive_resp()
        for _ in range(random.randint(0, 5)):
            await self.dut.AStep(1)

    async def main(self):
        for _ in range(10):
            await self.exec_once(is_push=True)
        for _ in range(10):
            await self.exec_once(is_push=False)

async def test_stack(stack):
    model = StackModel()

    port0 = SinglePortDriver(stack, model, {
        "in_valid": stack.in0_valid,
        "in_ready": stack.in0_ready,
        "in_data": stack.in0_data,
        "in_cmd": stack.in0_cmd,
        "out_valid": stack.out0_valid,
        "out_ready": stack.out0_ready,
        "out_data": stack.out0_data,
        "out_cmd": stack.out0_cmd,
    })

    port1 = SinglePortDriver(stack, model, {
        "in_valid": stack.in1_valid,
        "in_ready": stack.in1_ready,
        "in_data": stack.in1_data,
        "in_cmd": stack.in1_cmd,
        "out_valid": stack.out1_valid,
        "out_ready": stack.out1_ready,
        "out_data": stack.out1_data,
        "out_cmd": stack.out1_cmd,
    })

    asyncio.create_task(port0.main())
    asyncio.create_task(port1.main())
    await asyncio.create_task(stack.RunStep(200))

#并发执行: port0.main() 和 port1.main() 会并发地运行，因为它们没有被 await 立即等待。
#顺序等待: stack.RunStep(200) 会被创建为一个任务并立即开始执行，但是当前协程会等待这个任务完成之后再继续执行后续代码。

#if __name__ == "__main__":
#    dut = DUTdual_port_stack()
#    dut.InitClock("clk")
#    asyncio.run(test_stack(dut))
#    dut.Finish()
