# Python Data Generator

You're working on a medical administration application.
The back end involves a REST API, using the json-based [FHIR protocol](http://hl7.org/fhir/) to describe resources.
Your colleagues in the test automation team need lots of test data that they can send in their requests so they can check the responses.
They asked you to create a small application to generate test data efficiently.

The most important resources are Patient, Practitioner and Appointment, so these are in scope for now.

## Features

Please write a program with the following features.

1. Upon starting the data generator, the user is presented with a menu where they can choose what resource to generate.
2. User can also choose how many resources (json files) they want to generate (limiting the number to avoid a file flood is recommended).
3. The app generates the specified amount of data files and saves them in the `output` directory.

## Data format

A resource is a json file with a specified structure.
There are required fields but it is allowed to include more fields if necessary.
See example data in the `example_data` directory.

### Patient

| Key            | Value / Type                | Note             |
|----------------|-----------------------------|------------------|
| `resourceType` | 'Patient'                   | required         |
| `id`           | string                      | required, unique |
| `name`         | object                      | see example      |
| `gender`       | 'male' / 'female' / 'other' |                  |
| `birthDate`    | string (date)               | YYYY-mm-dd       |
| `address`      | object                      | see example      |

### Practitioner

| Key             | Value / Type   | Note             |
|-----------------|----------------|------------------|
| `resourceType`  | 'Practitioner' | required         |
| `id`            | string         | required, unique |
| `name`          | object         | see example      |
| `address`       | object         | see example      |
| `qualification` | object         | see example      |

### Appointment

| Key            | Value / Type                    | Note                |
|----------------|---------------------------------|---------------------|
| `resourceType` | 'Appointment'                   | required            |
| `id`           | string                          | required, unique    |
| `status`       | 'booked' / 'confirmed' / 'done' |                     |
| `class`        | 'ambulatory' / 'acute'          |                     |
| `description`  | string                          |                     |
| `start`        | string (date)                   | YYYY-mm-dd HH:MM:SS |
| `end`          | string (date)                   | YYYY-mm-dd HH:MM:SS |
| `created`      | string (date)                   | YYYY-mm-dd HH:MM:SS |

## Requirements

1. Id's must be different in all the generated files.
2. No more than 5 resources should have exactly the same names or other textual data.
3. Data files must be properly formatted json.
4. Please split your code into at leas 2 different modules.
5. All file operations should happen inside `with` statements.

## Optional tasks

1. Make it possible that appointments reference a patient and a practitioner by id. Enforce valid references (only existing id's).

Example:
```json
{
  "subject": {
    "reference": "Patient/patient_1",
    "display": "Eve Annabella Smith"
  },
  "participant": [{
    "reference": "Practitioner/practitioner_1",
    "display": "Prof Dr Adam Careful"
  }]
}
```

2. Make patient and practitioner references required when creating Appointment data.
3. Make it possible to create different resources without having to return to the main menu.

## Clean code reminder

Please always consider the principles of clean code.
In coding, going slower but cleaner is preferred over faster but dirtier.
If you decide to clean it up later, chances are it is never going to happen.
