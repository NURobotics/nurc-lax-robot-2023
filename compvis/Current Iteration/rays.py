import numpy as np

def ray_backtracking(Cam1, Cam2):
    cam_matrix = np.array([[506.84856584,   0,         319.76019864],
                            [0,         506.82585053,  238.71317098],
                            [0,           0,           1,        ]]) # hard coded from camera calibration
    if not (Cam1.x and Cam1.y and Cam2.x and Cam2.y):
        pass
    
    Ki_1 = np.linalg.inv(cam_matrix)
    ray1 = Ki_1.dot([Cam1.x, Cam1.y, 1.0])
    ray1_norm = np.linalg.norm(ray1)
    
    Ki_2 = np.linalg.inv(cam_matrix)
    ray2 = Ki_2.dot([Cam2.x, Cam2.y, 1.0])
    ray2_norm = np.linalg.norm(ray2)
    
    ray1_unit = ray1 / ray1_norm
    ray2_unit = ray2 / ray2_norm
    
    print(f"ray 1 unit vec {ray1_unit}")
    print(f"ray 2 unit vec {ray2_unit}")
    
    return (ray1_unit, ray2_unit)
    
    #cos_angle = ray1.dot(ray2) / (np.linalg.norm(ray1) * np.linalg.norm(ray2))
    #angle_radians = np.arccos(cos_angle)
    #angle_degrees = angle_radians * 180 / 3.141592