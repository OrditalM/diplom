class CameraConstants:
    def __init__(self, camera_choice='MAIN_CAMERA'):
        self.camera_choice = camera_choice

    @property
    def focal_length(self):
        if self.camera_choice == 'OV2640':
            return 0.00215
        elif self.camera_choice == 'OV2710':
            return 0.00369
        elif self.camera_choice == 'ISOCELL_GW3':
            return 0.025

    @property
    def matrix_y(self):
        if self.camera_choice == 'OV2640':
            return 3.59
        elif self.camera_choice == 'OV2710':
            return 5.85
        elif self.camera_choice == 'ISOCELL_GW3':
            return 6.5

    @property
    def matrix_x(self):
        if self.camera_choice == 'OV2640':
            return 2.68
        elif self.camera_choice == 'OV2710':
            return 3.27
        elif self.camera_choice == 'ISOCELL_GW3':
            return 4.86

    @property
    def image_size(self):
        if self.camera_choice == 'OV2640':
            return [800, 600]
        elif self.camera_choice == 'OV2710':
            return [1920, 1080]
        elif self.camera_choice == 'ISOCELL_GW3':
            return [1920, 1080]

    @property
    def fov(self):
        if self.camera_choice == 'OV2640':
            return 66
        elif self.camera_choice == 'OV2710':
            return 120
        elif self.camera_choice == 'ISOCELL_GW3':
            return 100

