#coding=utf8

try:
    from . import xspcomm as xsp
except Exception as e:
    import xspcomm as xsp

if __package__ or "." in __name__:
    from .libUT_adder import *
else:
    from libUT_adder import *


class DUTadder(object):

    # initialize
    def __init__(self, *args, **kwargs):
        self.dut = DutUnifiedBase(*args)
        self.xclock = xsp.XClock(self.dut.simStep)
        self.xport  = xsp.XPort()
        self.xclock.Add(self.xport)
        self.event = self.xclock.getEvent()
        self.internal_signals = {}
        # set output files
        if kwargs.get("waveform_filename"):
            self.dut.SetWaveform(kwargs.get("waveform_filename"))
        if kwargs.get("coverage_filename"):
            self.dut.SetCoverage(kwargs.get("coverage_filename"))

        # all Pins
        self.a_i = xsp.XPin(xsp.XData(4, xsp.XData.In), self.event)
        self.b_i = xsp.XPin(xsp.XData(4, xsp.XData.In), self.event)
        self.sum_o = xsp.XPin(xsp.XData(5, xsp.XData.Out), self.event)


        # BindDPI
        self.a_i.BindDPIPtr(self.dut.GetDPIHandle("a_i", 0), self.dut.GetDPIHandle("a_i", 1))
        self.b_i.BindDPIPtr(self.dut.GetDPIHandle("b_i", 0), self.dut.GetDPIHandle("b_i", 1))
        self.sum_o.BindDPIPtr(self.dut.GetDPIHandle("sum_o", 0), self.dut.GetDPIHandle("sum_o", 1))


        # Add2Port
        self.xport.Add("a_i", self.a_i.xdata)
        self.xport.Add("b_i", self.b_i.xdata)
        self.xport.Add("sum_o", self.sum_o.xdata)


        # Cascaded ports


    def __del__(self):
        self.Finish()

    ################################
    #         User APIs            #
    ################################
    def InitClock(self, name: str):
        self.xclock.Add(self.xport[name])

    def Step(self, i:int = 1):
        self.xclock.Step(i)

    def StepRis(self, callback, args=(), kwargs={}):
        self.xclock.StepRis(callback, args, kwargs)

    def StepFal(self, callback, args=(), kwargs={}):
        self.xclock.StepFal(callback, args, kwargs)

    def SetWaveform(self, filename: str):
        self.dut.SetWaveform(filename)
    
    def FlushWaveform(self):
        self.dut.FlushWaveform()

    def SetCoverage(self, filename: str):
        self.dut.SetCoverage(filename)
    
    def CheckPoint(self, name: str) -> int:
        self.dut.CheckPoint(name)

    def Restore(self, name: str) -> int:
        self.dut.Restore(name)

    def GetInternalSignal(self, name: str):
        if name not in self.internal_signals:
            signal = xsp.XData.FromVPI(self.dut.GetVPIHandleObj(name),
                                       self.dut.GetVPIFuncPtr("vpi_get"),
                                       self.dut.GetVPIFuncPtr("vpi_get_value"),
                                       self.dut.GetVPIFuncPtr("vpi_put_value"), name)
            if signal is None:
                return None
            self.internal_signals[name] = xsp.XPin(signal, self.event)
        return self.internal_signals[name]

    def VPIInternalSignalList(self, prefix="", deep=99):
        return self.dut.VPIInternalSignalList(prefix, deep)

    def Finish(self):
        self.dut.Finish()

    def RefreshComb(self):
        self.dut.RefreshComb()

    ################################
    #      End of User APIs        #
    ################################

    def __getitem__(self, key):
        return xsp.XPin(self.port[key], self.event)

    # Async APIs wrapped from XClock
    async def AStep(self,i: int):
        return await self.xclock.AStep(i)

    async def Acondition(self,fc_cheker):
        return await self.xclock.ACondition(fc_cheker)

    def RunStep(self,i: int):
        return self.xclock.RunStep(i)

    def __setattr__(self, name, value):
        assert not isinstance(getattr(self, name, None),
                              (xsp.XPin, xsp.XData)), \
        f"XPin and XData of DUT are read-only, do you mean to set the value of the signal? please use `{name}.value = ` instead."
        return super().__setattr__(name, value)


if __name__=="__main__":
    dut=DUTadder()
    dut.Step(100)
