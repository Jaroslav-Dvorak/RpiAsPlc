from time import sleep
from gpiozero import Button
from gpiozero.pins.pigpio import PiGPIOFactory
import snap7
from timers import TOF
from counter import Counter

rasp_ip = '10.10.8.1'


def is_rpi():
    try:
        with open('/sys/firmware/devicetree/base/model') as model:
            rpi_model = model.read()
    except FileNotFoundError:
        return False
    else:
        return rpi_model


class VirtualPLC:
    def __init__(self, ip):
        self.plc = snap7.client.Client()
        self.ip = ip
        while True:
            try:
                self.plc.connect(self.ip, 0, 2)
            except Exception as e:
                del e
                print("Virtual PLC server unavaible.")
                sleep(1)
            else:
                break


if is_rpi():
    virt_plc = VirtualPLC(ip='127.0.0.1')
    pin_factory = PiGPIOFactory(host='127.0.0.1')
else:
    virt_plc = VirtualPLC(ip=rasp_ip)
    pin_factory = PiGPIOFactory(host=rasp_ip)


def pls():
    RUN.trig()
    counter.value += 1
    print(counter.value)


HR1 = Button(pin=21,
             bounce_time=0.100,
             pin_factory=pin_factory,
             pull_up=False)
RUN = TOF(t=3)
HR1.when_pressed = pls

counter = Counter()


IDX_LIVEBIT = 4
IDX_RUN = 2
IDX_STOP = 0

IDX_R_LIVEBIT = 1

while True:
    to_wincc = bytearray(b'\x00'*49)
    from_wincc = virt_plc.plc.read_area(area=snap7.util.Areas.DB,
                                        dbnumber=200,
                                        start=50,
                                        size=1)

    livebit = snap7.util.get_bool(byte_index=0, bool_index=IDX_R_LIVEBIT, bytearray_=from_wincc)
    snap7.util.set_bool(value=livebit, byte_index=0, bool_index=IDX_LIVEBIT, bytearray_=to_wincc)

    snap7.util.set_bool(value=RUN.Q, byte_index=0, bool_index=IDX_RUN, bytearray_=to_wincc)
    snap7.util.set_bool(value=not RUN.Q, byte_index=0, bool_index=IDX_STOP, bytearray_=to_wincc)

    snap7.util.set_dword(dword=counter.value, byte_index=22, bytearray_=to_wincc)

    virt_plc.plc.write_area(area=snap7.util.Areas.DB,
                            dbnumber=200,
                            start=0,
                            data=to_wincc)

    sleep(0.5)
