import usb.core
import usb.util
import binascii
import time
from array import array

# find the FX3 device
dev = usb.core.find(idVendor=0x1331, idProduct=0x1005)

if dev is None:
    raise ValueError('Device not found')
else:
    try:
        xdev = usb.core.find(idVendor=dev.idVendor, idProduct=dev.idProduct)
        if xdev._manufacturer is None:
            xdev._manufacturer = usb.util.get_string(xdev, xdev.iManufacturer)
        if xdev._product is None:
            xdev._product = usb.util.get_string(xdev, xdev.iProduct)
        stx = '%4x %4x: '+str(xdev._manufacturer).strip()+' = '+str(xdev._product).strip()
        print (stx % (dev.idVendor,dev.idProduct))
        print ('Bus: ' +  str(dev.bus) + ' Address: ' + str(dev.address))
    except:
        print ('Cannot print device name!')
# set the active configuration of the device

print('Configurazioni:')
for cfg in dev:
    print ('\t' + str(cfg.bConfigurationValue))
    for intf in cfg:
        print ('\t' + \
                         str(hex(intf.bInterfaceNumber)) + \
                         ',' + \
                         str(hex(intf.bAlternateSetting)))
        print ('\tEndpoints:')
        for ep in intf:
            print ('\t\t' + \
                             str('Address: ' + hex(ep.bEndpointAddress)) + ' Direction: ' + hex(usb.util.endpoint_direction(ep.bEndpointAddress)) + ' Address: ' + hex(usb.util.endpoint_address(ep.bEndpointAddress)) + ' Type: ' + hex(usb.util.endpoint_type(ep.bEndpointAddress)) )

dev.set_configuration()

# claim the interface for communication
interface = 0
usb.util.claim_interface(dev, interface)
ultimo = 0
primo = 0
running = False
while True:
     
    response = dev.read(0x82, 1024)
    primo = response[0]
    
    if running:
        if ultimo == primo:
            #print ('ok');
            pass
        else:
            print('no ' + str(ultimo) + ' ' + str(primo))    
    else:
        running = True
    
    #lenResponse = len(response)

    #print(response)


    #print (str(lenResponse) + ' bytes')
    ultimo = response[-1] + 1
    if ultimo == 256:
        ultimo = 0
    
# release the interface
usb.util.release_interface(dev, interface)

# Dispose the device resource
usb.util.dispose_resources(dev)
