import json
from datetime import datetime, timedelta


class BaseGenerator:
    def __init__(self, count, output_dir):
        self.count = count
        self.output_dir = output_dir

    def generate_data(self):
        for i in range(1, self.count + 1):
            resource_data = self.generate_resource_data(i)
            self.save_to_file(resource_data, f"{self.output_dir}/resource_{i}.json")

    @staticmethod
    def save_to_file(data, file_path):
        with open(file_path, "w") as file:
            json.dump(data, file, indent=2)

    def generate_resource_data(self, resource_id):
        raise NotImplementedError("Subclasses must implement generate_resource_data")


class PatientGenerator(BaseGenerator):
    def generate_resource_data(self, resource_id):
        return {
            "resourceType": "Patient",
            "id": f"patient_{resource_id}",
            "name": {"given": f"Patient{resource_id}", "family": "Smith"},
            "gender": "male" if resource_id % 2 == 0 else "female",
            "birthDate": (datetime.now() - timedelta(days=365 * 30 * resource_id)).strftime("%Y-%m-%d"),
            "address": {"city": "City" + str(resource_id), "state": "State" + str(resource_id)},
        }


class PractitionerGenerator(BaseGenerator):
    def generate_resource_data(self, resource_id):
        return {
            "resourceType": "Practitioner",
            "id": f"practitioner_{resource_id}",
            "name": {"given": f"Dr{resource_id}", "family": "Careful"},
            "address": {"city": "City" + str(resource_id), "state": "State" + str(resource_id)},
            "qualification": {"code": f"Q{resource_id}", "description": "Qualification Description"},
        }


class AppointmentGenerator(BaseGenerator):
    def generate_resource_data(self, resource_id):
        return {
            "resourceType": "Appointment",
            "id": f"appointment_{resource_id}",
            "status": "booked",
            "class": "ambulatory" if resource_id % 2 == 0 else "acute",
            "description": f"Appointment Description {resource_id}",
            "start": (datetime.now() + timedelta(days=resource_id)).strftime("%Y-%m-%d %H:%M:%S"),
            "end": (datetime.now() + timedelta(days=resource_id + 1)).strftime("%Y-%m-%d %H:%M:%S"),
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
