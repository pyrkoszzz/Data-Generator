import random

import pytest
from datetime import datetime, timedelta
from data_generator import PatientGenerator, PractitionerGenerator, AppointmentGenerator, fake


@pytest.fixture
def patient_generator():
    return PatientGenerator(1, 'output')


@pytest.fixture
def practitioner_generator():
    return PractitionerGenerator(1, 'output')


@pytest.fixture
def appointment_generator():
    return AppointmentGenerator(1, 'output')


def test_patient_generator(monkeypatch, patient_generator):
    fake_uuid = "fake_uuid_value"
    monkeypatch.setattr("uuid.uuid4", lambda: fake_uuid)

    fake_first_name = "John"
    fake_last_name = "Doe"
    fake_street_address = "123 Main St"
    fake_zipcode = "12345"
    fake_gender = "male"
    fake_birth_date = "1990-01-01"

    monkeypatch.setattr(fake, "first_name", lambda: fake_first_name)
    monkeypatch.setattr(fake, "last_name", lambda: fake_last_name)
    monkeypatch.setattr(fake, "street_address", lambda: fake_street_address)
    monkeypatch.setattr(fake, "zipcode", lambda: fake_zipcode)
    monkeypatch.setattr(fake, "random_element", lambda elements: elements[0])
    monkeypatch.setattr(fake, "date_of_birth",
                        lambda minimum_age, maximum_age: datetime.strptime(fake_birth_date, "%Y-%m-%d"))

    generated_data = patient_generator.generate_resource_data()

    assert generated_data["resourceType"] == "Patient"
    assert generated_data["id"] == f"patient_{fake_uuid}"
    assert generated_data["name"][0]["given"] == [fake_first_name, fake_first_name]
    assert generated_data["name"][0]["family"] == fake_last_name
    assert generated_data["gender"] == fake_gender
    assert generated_data["birthDate"] == fake_birth_date
    assert generated_data["address"][0]["line"] == [fake_street_address]
    assert generated_data["address"][0]["postalCode"] == fake_zipcode


def test_practitioner_generator(monkeypatch, practitioner_generator):
    fake_uuid = "fake_uuid_value"
    monkeypatch.setattr("uuid.uuid4", lambda: fake_uuid)

    fake_last_name = "Smith"
    fake_first_name = "Jane"
    fake_street_address = "456 Oak St"
    fake_city = "City"
    fake_state_abbr = "ST"
    fake_zipcode = "54321"
    fake_company = "Medical Center"

    monkeypatch.setattr(fake, "last_name", lambda: fake_last_name)
    monkeypatch.setattr(fake, "first_name", lambda: fake_first_name)
    monkeypatch.setattr(fake, "street_address", lambda: fake_street_address)
    monkeypatch.setattr(fake, "city", lambda: fake_city)
    monkeypatch.setattr(fake, "state_abbr", lambda: fake_state_abbr)
    monkeypatch.setattr(fake, "zipcode", lambda: fake_zipcode)
    monkeypatch.setattr(fake, "company", lambda: fake_company)

    generated_data = practitioner_generator.generate_resource_data()

    assert generated_data["resourceType"] == "Practitioner"
    assert generated_data["id"] == f"practitioner_{fake_uuid}"
    assert generated_data["name"][0]["family"] == fake_last_name
    assert generated_data["name"][0]["given"] == [fake_first_name, fake_first_name]
    assert generated_data["address"][0]["line"] == [fake_street_address]
    assert generated_data["address"][0]["city"] == fake_city
    assert generated_data["address"][0]["state"] == fake_state_abbr
    assert generated_data["address"][0]["postalCode"] == fake_zipcode
    assert generated_data["qualification"][0]["issuer"]["display"] == fake_company


def test_appointment_generator(monkeypatch, appointment_generator):
    fake_uuid = "fake_uuid_value"
    monkeypatch.setattr("uuid.uuid4", lambda: fake_uuid)

    fake_sentence = "Lorem ipsum dolor sit amet"
    fake_date_time = datetime(2024, 1, 1, 12, 0, 0)
    fake_random_int = 1

    monkeypatch.setattr(fake, "sentence", lambda: fake_sentence)
    monkeypatch.setattr(fake, "random_element", lambda elements: elements[0])
    monkeypatch.setattr(fake, "date_time_this_year", lambda: fake_date_time)
    monkeypatch.setattr(random, "randint", lambda a, b: fake_random_int)

    generated_data = appointment_generator.generate_resource_data()

    assert generated_data["resourceType"] == "Appointment"
    assert generated_data["id"] == f"appointment_{fake_uuid}"
    assert generated_data["status"] in ['booked', 'confirmed', 'done']
    assert generated_data["class"] in ['ambulatory', 'acute']
    assert generated_data["description"] == fake_sentence
    assert generated_data["start"] == fake_date_time.strftime("%Y-%m-%d %H:%M:%S")
    assert generated_data["end"] == (fake_date_time + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    assert generated_data["created"] == fake_date_time.strftime("%Y-%m-%d %H:%M:%S")
