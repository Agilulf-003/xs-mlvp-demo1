from toffee import *
from .axi4_bundle import *

class AXI4Config:
    FIXED, INCR, WARP = 0, 1, 2
    OKAY, EXOKAY, SLVERR, DECERR = 0, 1, 2, 3
    AxSIZE = 0x3
    BURST_TYPE = INCR

class AXI4MasterAgent(Agent):
    async def send_addr(self, port: Bundle, addr, len, size, burst_type, id=0):
        assert (addr & ((1 << size) - 1)) == 0, "Address must be aligned to size"
        assert len >= 0, "Length must be non-negative"
        port.assign({"valid": 1, "addr": addr, "len": len, "size": size, "burst": burst_type})
        with open ('/home/haom/work/xs/xs-mlvp-demo1/toffee-cases/axi4/toffee/test_out.txt','a') as f:
            print("test_agent_sendaddr_16",file=f)
        await AllValid(port.ready)
        with open ('/home/haom/work/xs/xs-mlvp-demo1/toffee-cases/axi4/toffee/test_out.txt','a') as f:
            print("test_agent_sendaddr_19",file=f)

        port.valid.value = 0

    @driver_method()
    async def read(self, addr, len):
        with open ('/home/haom/work/xs/xs-mlvp-demo1/toffee-cases/axi4/toffee/test_out.txt','a') as f:
            print("test_agent_read_26",file=f)
        await self.send_addr(self.bundle.ar, addr, len - 1, AXI4Config.AxSIZE, AXI4Config.BURST_TYPE)
        with open ('/home/haom/work/xs/xs-mlvp-demo1/toffee-cases/axi4/toffee/test_out.txt','a') as f:
            print("test_agent_read_29",file=f)
        read_data = []
        self.bundle.r.ready.value = 1
        while True:
            if self.bundle.r.valid.value and self.bundle.r.ready.value:
                read_data.append(self.bundle.r.data.value)
                if self.bundle.r.last.value:
                    break
            await ClockCycles(self.bundle)
        self.bundle.r.ready.value = 0
        return read_data

    @driver_method()
    async def write(self, addr, data):
        await self.send_addr(self.bundle.aw, addr, len(data) - 1, AXI4Config.AxSIZE, AXI4Config.BURST_TYPE)
        for i in range(len(data)):
            self.bundle.w.assign({"valid": 1, "data": data[i], "last": i == len(data) - 1, "strb": 0xFF})
            await AllValid(self.bundle.w.ready)
            self.bundle.w.valid.value = 0
        self.bundle.b.ready.value = 1
        await AllValid(self.bundle.b.valid)
        self.bundle.b.ready.value = 0
        return self.bundle.b.resp.value
