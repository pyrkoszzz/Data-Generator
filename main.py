from data_generator import PatientGenerator, PractitionerGenerator, AppointmentGenerator
from decorators import validate_input


@validate_input
def get_user_choice():
    return int(input("Enter your choice (1-4): "))


@validate_input
def get_resource_count():
    return int(input("Enter the number of resources to generate: "))


def generate_data(generator_cls, output_dir):
    count = get_resource_count()
    generator = generator_cls(count, output_dir)
    generator.generate_data()


def exit_program():
    print("Exiting program.")
    exit()


def main():
    menu_options = {
        1: {"function": generate_data, "args": (PatientGenerator, "patients"), "message": "Generate Patient Data"},
        2: {"function": generate_data, "args": (PractitionerGenerator, "practitioners"),
            "message": "Generate Practitioner Data"},
        3: {"function": generate_data, "args": (AppointmentGenerator, "appointments"),
            "message": "Generate Appointment Data"},
        4: {"function": exit_program, "args": (), "message": "Exit Program"},
    }
    while True:
        for option, data in menu_options.items():
            print(f"{option}. {data['message']}")

        choice = get_user_choice()

        if choice in menu_options:
            menu_option = menu_options[choice]
            menu_option["function"](*menu_option["args"])
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
