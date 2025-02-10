from adder import *
import random

# 生成无符号随机数
def random_int():
    return random.randint(-(2**3), 2**3 - 1) & ((1 << 3) - 1)

# 通过python实现的加法器参考模型
def reference_adder(a, b):
    sum = (a + b) & ((1 << 4) - 1)
    return sum

def random_test():
    # 创建DUT
    dut = DUTadder()
    # 默认情况下，引脚赋值不会立马写入，而是在下一次时钟上升沿写入，这对于时序电路适用，但是Adder为组合电路，所以需要立即写入
    #   因此需要调用AsImmWrite()方法更改引脚赋值行为
    dut.a_i.AsImmWrite()
    dut.b_i.AsImmWrite()
    # 循环测试
    for i in range(114514):
        a, b= random_int(), random_int()
        # DUT：对Adder电路引脚赋值，然后驱动组合电路 （对于时序电路，或者需要查看波形，可通过dut.Step()进行驱动）
        dut.a_i.value, dut.b_i.value = a, b
        dut.RefreshComb() #TODO
        # 参考模型：计算结果
        ref_sum = reference_adder(a, b)
        # 检查结果
        assert dut.sum_o.value == ref_sum, "sum mismatch: 0x{dut.sum.value:x} != 0x{ref_sum:x}"
        print(f"[test {i}] a=0x{a:x}, b=0x{b:x} => sum: 0x{ref_sum}")
    # 完成测试
    dut.Finish()
    print("Test Passed")

#if __name__ == "__main__":
#    random_test()
