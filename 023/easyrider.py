import json
import re


class Main:
    def __init__(self):
        self.errors = {'bus_id': 0,
                       'stop_id': 0,
                       'stop_name': 0,
                       'next_stop': 0,
                       'stop_type': 0,
                       'a_time': 0}
        self.total = 0
        self.start()

    def start(self):
        user = input()
        bus_dict = json.loads(user)
        self.check_input(bus_dict)
        print(f"Type and required field validation: {self.total} errors")
        for error_id, error in self.errors.items():
            print(f"{error_id}: {error}")

    def check_input(self, bus_dict):
        for bus in bus_dict:
            if not isinstance(bus['bus_id'], int):
                self.errors['bus_id'] += 1
            if not isinstance(bus['stop_id'], int):
                self.errors['stop_id'] += 1
            if not bus['stop_name'] or not isinstance(bus['stop_name'], str):
                self.errors['stop_name'] += 1
            if not isinstance(bus['next_stop'], int):
                self.errors['next_stop'] += 1
            if not isinstance(bus['stop_type'], str) or len(bus['stop_type']) > 1:
                self.errors['stop_type'] += 1
            if not bus['a_time'] or not isinstance(bus['a_time'], str):
                self.errors['a_time'] += 1
        for error in self.errors.values():
            self.total += error


if __name__ == '__main__':
    Main()
