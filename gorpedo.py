import usb.core
import usb.util


class TorpedoDevice:
    vendor_id = 0x0483
    device_id = 0xa334

    def __init__(self):
        self.serial_number = None
        self.device = None

    def find_device(self):
        r"""Find the USB device according to the
        defined vendor and device ID.
        """
        result = usb.core.find(idVendor=self.vendor_id, idProduct=self.device_id)

        if result is not None:
            if result.manufacturer == "Two Notes Audio Engineering" and \
                    result.product == "Torpedo Live":
                self.device = result
                self.serial_number = result.serial_number
                return True
        else:
            return False

    def setup_device(self):
        r"""
        """
        config_count = 1
        for config in self.device:
            for i in range(config.bNumInterfaces):
                if self.device.is_kernel_driver_active(i):
                    self.device.detach_kernel_driver(i)
        config_count += 1

        self.device.set_configuration()

    def test(self):
        for cfg in self.device:
            for intf in cfg:
                print(str(intf))
                for ep in intf:
                    print(str(ep))

    def test2(self):
        self.device.write(0x81, [], 0)
        test = self.device.read(0x81, 64)
        print(test)


torpedo = TorpedoDevice()

if torpedo.find_device():
    torpedo.setup_device()
    # torpedo.test()
    torpedo.test2()
