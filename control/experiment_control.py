from .arduino_control import ArduinoControl
from .vision_control import VisionControl


class ExperimentControl:
    def __init__(self):
        self.prepare_experiment()

    def prepare_experiment(self):
        self._arduino_control = ArduinoControl()
        self._vision_control = VisionControl()

    def get_force_reading(self):
        return self._arduino_control.read_sensor()

    def get_measured_distance(self):
        return self._vision_control.get_measurement()

    def increase_stress(self):
        self._arduino_control.spin_motor_anticlockwise()

    def decrease_stress(self):
        self._arduino_control.spin_motor_clockwise()

    def start_experiment(self):
        self._vision_control.start_processing()
        self._arduino_control.start_motor()

    def stop_experiment(self):
        self._vision_control.stop_processing()
        self._arduino_control.stop_motor()

    def adjust_focus(self):
        self._vision_control.adjust_camera_focus()

    def calibrate(self):
        self._vision_control.calibrate_camera()


def __testing():
    from modules.timer import TimerSeconds
    import time

    experiment_ctrl = ExperimentControl()

    experiment_ctrl.start_experiment()
    timer = TimerSeconds()
    while timer.elapsed_time() < 5:
        try:
            # experiment_ctrl.decrease_stress()
            print(experiment_ctrl.get_force_reading(), experiment_ctrl.get_measured_distance())
        except Exception as exc:
            print(f"{exc}")
        time.sleep(0.5)
    experiment_ctrl.stop_experiment()

if __name__ == "__main__":
    __testing()
