import os
import json
import random
from datetime import timedelta
from faker import Faker
import uuid

fake = Faker()


class BaseGenerator:
    def __init__(self, count, output_dir):
        self.count = max(count, 10)
        self.output_dir = output_dir

    def generate_data(self):
        for i in range(1, self.count + 1):
            resource_data = self.generate_resource_data()
            file_name = f"{self.output_dir}/{resource_data['id']}.json"
            self.save_to_file(resource_data, file_name)

    @staticmethod
    def save_to_file(data, file_path):
        with open(file_path, "w") as file:
            json.dump(data, file, indent=2)

    def generate_resource_data(self):
        raise NotImplementedError("Subclasses must implement generate_resource_data")


class PatientGenerator(BaseGenerator):
    def generate_resource_data(self):
        return {
            "resourceType": "Patient",
            "id": f"patient_{str(uuid.uuid4())}",
            "name": [
                {
                    "use": "official",
                    "given": [fake.first_name(), fake.first_name()],
                    "family": fake.last_name()
                }
            ],
            "gender": fake.random_element(elements=('male', 'female', 'other')),
            "birthDate": fake.date_of_birth(minimum_age=20, maximum_age=80).strftime("%Y-%m-%d"),
            "address": [
                {
                    "use": "home",
                    "line": [fake.street_address()],
                    "postalCode": fake.zipcode()
                }
            ]
        }


class PractitionerGenerator(BaseGenerator):
    def generate_resource_data(self):
        practitioner_id = f"practitioner_{uuid.uuid4()}"
        return {
            "resourceType": "Practitioner",
            "id": practitioner_id,
            "name": [
                {
                    "family": fake.last_name(),
                    "given": [fake.first_name(), fake.first_name()],
                    "prefix": ["Prof", "Dr"],
                }
            ],
            "address": [
                {
                    "use": "home",
                    "line": [fake.street_address()],
                    "city": fake.city(),
                    "state": fake.state_abbr(),
                    "postalCode": fake.zipcode(),
                }
            ],
            "qualification": [
                {
                    "code": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0360/2.7",
                                "code": "DM",
                                "display": "Doctor of Medicine",
                            }
                        ],
                        "text": "Doctor of Medicine",
                    },
                    "issuer": {
                        "display": fake.company()
                    },
                }
            ],
        }


class AppointmentGenerator(BaseGenerator):
    def generate_resource_data(self):
        return {
            "resourceType": "Appointment",
            "id": f"appointment_{str(uuid.uuid4())}",
            "status": fake.random_element(elements=('booked', 'confirmed', 'done')),
            "class": fake.random_element(elements=('ambulatory', 'acute')),
            "description": fake.sentence(),
            "start": fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S"),
            "end": (fake.date_time_this_year() + timedelta(hours=random.randint(1, 3))).strftime("%Y-%m-%d %H:%M:%S"),
            "created": fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S"),
        }
