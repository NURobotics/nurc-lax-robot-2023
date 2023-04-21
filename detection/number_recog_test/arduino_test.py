import pyduino as pyd

if __name__ == '__main__':
    x = float(input('\nEnter x coord: ' ))
    y = float(input('\nEnter y coord: '))

    cv_coords = [x,y]
    robot_coords = pyd.convert_coords(cv_coords)

    j1, j2, j3 = pyd.inverse_kinematics(robot_coords[0], robot_coords[1])
    z = 0
    gripper = 90


    arduino_txt = pyd.format_commands(j1,j2,j3,z,gripper)
    result = pyd.write_read_arduino(arduino_txt)
