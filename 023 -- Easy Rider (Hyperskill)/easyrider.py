import json
import re


class DataValidator:
    def __init__(self):
        self.errors = {'bus_id': 0,
                       'stop_id': 0,
                       'stop_name': 0,
                       'next_stop': 0,
                       'stop_type': 0,
                       'a_time': 0}
        self.format_errors = {'stop_name': 0,
                              'stop_type': 0,
                              'a_time': 0}

    @property
    def total(self):
        return sum(self.errors.values())

    @property
    def ftotal(self):
        return sum(self.format_errors.values())

    def check_input(self, data, verbose=False):
        for bus in data:
            if not isinstance(bus['bus_id'], int):
                self.errors['bus_id'] += 1
            if not isinstance(bus['stop_id'], int):
                self.errors['stop_id'] += 1
            if not isinstance(bus['stop_name'], str):
                self.errors['stop_name'] += 1
            else:
                self.check_data_format('stop_name', bus['stop_name'])
            if not isinstance(bus['next_stop'], int):
                self.errors['next_stop'] += 1
            if bus['stop_type'] and not isinstance(bus['stop_type'], str):
                self.errors['stop_type'] += 1
            elif bus['stop_type']:
                self.check_data_format('stop_type', bus['stop_type'])
            if not isinstance(bus['a_time'], str):
                self.errors['a_time'] += 1
            else:
                self.check_data_format('a_time', bus['a_time'])
        if verbose:
            print(f"Type and required field validation: {self.total} errors")
            for error_id, error in self.errors.items():
                print(f"{error_id}: {error}")
            print(f"Format validation: {self.ftotal} errors")
            for err_id, err in self.format_errors.items():
                print(f"{err_id}: {err}")

    def check_data_format(self, key, bus_data):
        pattern = ''
        if key == 'stop_name':
            pattern = '^[A-Z][A-z ]+(Road|Avenue|Boulevard|Street)$'
        elif key == 'stop_type':
            pattern = '^[SOF]$'
        elif key == 'a_time':
            pattern = '^(0[1-9]|1[0-9]|2[0-3]):([0-5][0-9])$'
        if not re.match(pattern, bus_data):
            self.format_errors[key] += 1


class Bus:
    def __init__(self, bus_id):
        self.id = bus_id
        self.stops = dict()
        self.start_stop = None
        self.final_stop = None

    @property
    def nstops(self):
        return len(self.stops)

    @property
    def stop_ids(self):
        return list(self.stops.keys())

    @property
    def a_times(self):
        return list(self.stops.values())


class EasyRider:
    def __init__(self):
        self.stops = dict()
        self.buses = dict()
        self.start_stops = set()
        self.transfer_stops = set()
        self.final_stops = set()
        self.start()

    def start(self):
        input_data = json.loads(input())
        DataValidator().check_input(input_data, verbose=False)
        self.create_lines_dict(input_data)
        self.create_stops_info(verbose=False)
        self.check_a_times(verbose=True)

    def create_lines_dict(self, input_data):
        for data in input_data:
            bid = data['bus_id']
            stopid = data['stop_id']
            if bid not in self.buses.keys():
                self.buses[bid] = Bus(bid)
            self.buses[bid].stops[stopid] = data['a_time']
            if data['stop_type'] == 'S':
                self.buses[bid].start_stop = data['stop_id']
            elif data['stop_type'] == 'F':
                self.buses[bid].final_stop = data['stop_id']
            if stopid not in self.stops.keys():
                self.stops[stopid] = data['stop_name']

    def create_stops_info(self, verbose=False):
        lines = list()
        for bus in self.buses.values():
            if not bus.start_stop or not bus.final_stop:
                print(f"There is no start or end stop for the line {bus.id}")
                exit()
            self.start_stops.add(self.stops[bus.start_stop])
            self.final_stops.add(self.stops[bus.final_stop])
            lines.extend(bus.stops)
        for line in lines:
            if lines.count(line) > 1:
                self.transfer_stops.add(self.stops[line])
        if verbose:
            print(f"Start stops: {len(self.start_stops)} {sorted(self.start_stops)}")
            print(f"Transfer stops: {len(self.transfer_stops)} {sorted(self.transfer_stops)}")
            print(f"Finish stops: {len(self.final_stops)} {sorted(self.final_stops)}")

    def check_a_times(self, verbose=False):
        errors = dict()
        for bus in self.buses.values():
            for i in range(bus.nstops - 1):
                if bus.a_times[i] > bus.a_times[i + 1]:
                    errors[bus.id] = bus.stop_ids[i + 1]
                    break
        if verbose:
            print("Arrival time test:")
            if not errors:
                print("OK")
            else:
                for bus_id, stop_id in errors.items():
                    print(f"bus _id line {bus_id}: wrong time on station {self.stops[stop_id]}")


if __name__ == '__main__':
    EasyRider()
