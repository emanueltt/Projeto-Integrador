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

    def adjust_focus(self, focus_value: int):
        self._vision_control.adjust_camera_focus(focus_value)

    def calibrate(self):
        self._vision_control.calibrate_camera()


def _focus_adjusting():
    from modules.timer import TimerSeconds
    import cv2

    vision_control = VisionControl()
    vision_control.start_processing()

    timer = TimerSeconds()
    focus = 5
    changed = True
    print("Pressione ESC para parar. Utilize as setas para esquerda e direita para ajustar o foco")
    while timer.elapsed_time() < 120:
        try:
            frame = vision_control._image_queue.get()
            if frame is not None:
                cv2.imshow("image", frame)

            key = cv2.waitKey(1)
            if key == 27:
                break
            elif key == 81:
                focus -= 1
                changed = True
            elif key == 83:
                focus += 1
                changed = True
            # else:
            #     print(key)
            if changed:
                print(f"Foco atual: {focus}")
                vision_control.adjust_camera_focus(focus)
                changed = False
        except Exception as exc:
            print(f"{exc}")
    cv2.destroyAllWindows()


def _test_experiment():
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
    _focus_adjusting()
