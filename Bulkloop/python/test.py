import usb.core
import usb.util
import binascii
from array import array
import random

# find the FX3 device
dev = usb.core.find(idVendor=0x04b4, idProduct=0x1005)

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
        pass
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

# send a command to the device conta avanti
cmd = [0x0, 0x02, 0x01]
# send a command to the device conta indietro
#cmd = [0x1, 0x02, 0x01]
# send a unknow command
#cmd = [0x2, 0x02, 0x01]

dev.write(2, cmd)
print("Comando", cmd)

# read a response from the device
try:
    response = dev.read(0x86, 512)
except:
    print("Errore in ricezione usb")
    response = []

print("Risposta", response)

cmd = array('B', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                  24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
                  46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67,
                  68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89,
                  90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109,
                  110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128,
                  129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147,
                  148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166,
                  167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185,
                  186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204,
                  205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223,
                  224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242,
                  243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                  10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                  34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57,
                  58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81,
                  82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104,
                  105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123,
                  124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142,
                  143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161,
                  162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180,
                  181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199,
                  200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218,
                  219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237,
                  238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255])

lenOrig = len(cmd)
lenResponse = len(response)

if cmd == response:
    print ('OK ' + str(lenOrig) + ' bytes')
else:
    print ('Error out ' + str(lenOrig) + ' bytes in ' + str(lenResponse) + ' bytes'  ) 


#try:
#    response = dev.read(0x86, 512)
#    print(response)
#except:
#    pass

random.seed()

cmd = array('B', [])

#max txcount is 2048 that is 4 fx2lp usb busses x 512 bus dimensions
txcount = 2048

for index in range(txcount):
    cmd.append(random.randint(0,255))
 
lenOrig = len(cmd)
dev.write(4, cmd)

# read a response from the device
response = dev.read(0x88, lenOrig)
lenResponse = len(response)

print (cmd)

print(response)

if cmd == response:
    print ('OK ' + str(lenOrig) + ' bytes')
else:
    print ('Error out ' + str(lenOrig) + ' bytes in ' + str(lenResponse) + ' bytes'  )

# release the interface
usb.util.release_interface(dev, interface)

# Dispose the device resource
usb.util.dispose_resources(dev)
