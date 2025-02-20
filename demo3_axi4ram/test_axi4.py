
import random
from toffee import *
import toffee_test
from UT_AXI4RAM import DUTAXI4RAM
from axi4_env import AXI4Bundle, AXI4Env
from hypothesis import given, settings, HealthCheck, strategies as st

@toffee_test.testcase
async def test_read_once(axi4_env: AXI4Env):
    for _ in range(100):
        await axi4_env.in_agent.read(random.randint(0, (1<<12)-1) >> 3 << 3, 1)
        #with open ('/home/haom/work/xs/xs-mlvp-demo1/toffee-cases/axi4/toffee/test_out.txt','a') as f:
        #    print("test_case0_16",file=f)

@toffee_test.testcase
async def test_read_burst(axi4_env: AXI4Env):
    for _ in range(1000):
        await axi4_env.in_agent.read(random.randint(0, (1<<11)-1) >> 3 << 3, random.randint(1, 16))

@toffee_test.testcase
async def test_write_once(axi4_env: AXI4Env):
    for _ in range(3000):
        await axi4_env.in_agent.write(random.randint(0, (1<<12)-1) >> 3 << 3, [random.randint(0, (1<<64)-1)])

@toffee_test.testcase
async def test_write_burst(axi4_env: AXI4Env):
    for _ in range(1000):
        await axi4_env.in_agent.write(
            random.randint(0, (1<<11)-1) >> 3 << 3,
            [random.randint(0, (1<<64)-1) for _ in range(random.randint(1, 16))])

@toffee_test.testcase
async def test_read_and_write_same_addr(axi4_env: AXI4Env):
    for _ in range(5000):
        addr = random.randint(0, (1<<11)-1) >> 3 << 3
        data = [random.randint(0, (1<<64)-1) for _ in range(random.randint(1, 16))]
        await axi4_env.in_agent.write(addr, data)
        await axi4_env.in_agent.read(addr, len(data))

#@toffee_test.testcase
#async def test_random_read_and_write(axi4_env: AXI4Env):
#    for _ in range(10000):
#        addr = random.randint(0, (1<<10)-1) >> 3 << 3
#        data = [random.randint(0, (1<<64)-1) for _ in range(random.randint(1, 16))]
#        if random.choice([True, False]):
#            await axi4_env.in_agent.write(addr, data)
#        else:
#            await axi4_env.in_agent.read(addr, len(data))

#通过将fixture声明为参数名，测试用例函数可以请求fixture。
#fixture修饰器来标记固定的工厂函数,在其他函数，模块，类或整个工程调用它时会被激活并优先执行,通常会被用于完成预置处理和重复操作
@toffee_test.fixture
async def axi4_env(toffee_request: toffee_test.ToffeeRequest):
    dut = toffee_request.create_dut(DUTAXI4RAM, "clock", "AXI4RAM.fst") #init clock here
    start_clock(dut)  #toffee的时钟函数#
    return AXI4Env(dut)


#@toffee_test.fixture()
#def dut_input(request):
#    # before test
#    #init_function_coverage(g)
#    dut = DUT()
#    dut.InitClock("clock")
#    dut.StepRis(lambda x: g.sample())
#
#    yield dut
#    # after test
#    dut.Finish()
#    #set_func_coverage(request, g)
#    g.clear()

#The dut_input fixture is defined but not requested by any test case.
#Therefore, it will not be executed as part of the test suite unless some external code or test case (not shown) requests it.