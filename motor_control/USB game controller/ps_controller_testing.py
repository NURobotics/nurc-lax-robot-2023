#import hid

#for device in hid.enumerate():
#    print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")
   
import time
import hid

# Set up HID device
VENDOR_ID = 0x0079
PRODUCT_ID = 0x0006
device = hid.device()
device.open(VENDOR_ID, PRODUCT_ID)

MOTOR_SPEED = 100

# Read data every 0.1 seconds
while True:
    # Read input report
    report = device.read(64)
    xraw = report[0]
    yraw = report[1]

    #convert to normalized x and y vectors
    x =  (xraw-128)/128
    y = -(yraw-128)/128

    #convert to motor rotations
    M1 =  (x-y) * MOTOR_SPEED
    M2 = (-x-y) * MOTOR_SPEED
    
    # Parse the data and print it to the console
    print(f'Unscaled values: ({xraw}, {yraw})  ' + \
            f'Scaled: ({round(x,3)}, {round(y,3)})  ' + \
            f'Mot. speed: ({int(M1)}, {int(M2)})')

    '''
    Button mapping (note: press the "Analog Mode" button on the controller
    for these results; otherwise it's different):
    - Report[0]: Joystick 1 X
    - Report[1]: Joystick 1 Y
    - Report[2]
    - Report[3]: Joystick 2 X
    - Report[4]: Joystick 2 Y
    - Report[5]: bitwise stuff for
        - buttons 1,2,3,4
        - D-pad up/down/left/right
    - Report[6]: bitwise stuff for
        - Select + Start
        - Shoulder buttons

    '''

    time.sleep(0.001)


