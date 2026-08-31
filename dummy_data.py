import json
import random
from faker import Faker
from faker.providers import BaseProvider


class GenderProvider(BaseProvider):
    def gender(self):
        return random.choice(["Male", "Female", "Non-binary"])


def generate_mock_patient_data(num_records: int) -> list:
    fake = Faker()
    patient_list = []
    gender_options = ["Male", "Female"]
    fake.add_provider(GenderProvider)
    for i in range(1, num_records + 1):
        gender = random.choice(gender_options)
        patient_profile = {
            "id": i,
            "name" : fake.name_male() if gender == "Male" else fake.name_female(),
            "city": fake.city(),
            "age" : fake.random_int(1, 100),
            "gender": fake.gender(),
            "phone_number": fake.phone_number(),
            "weight" : fake.random_int(1, 100),
            "height": fake.random_int(4, 10)
        }
        patient_list.append(patient_profile)
    return patient_list

def save_to_json_file(data: list, filename: str):
    """Serializes Python list/dictionary data and writes it to a JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            # indent=4 formats the JSON cleanly; sort_keys sorts the dictionary keys alphabetically
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"✅ Successfully generated and saved {len(data)} records to '{filename}'")
    except IOError as e:
        print(f"❌ Error writing to file: {e}")


if __name__ == "__main__":
    # Define how many dummy records you want to generate
    RECORD_COUNT = 100
    OUTPUT_FILE = "./data/dummy_users.json"
    dummy_data = generate_mock_patient_data(RECORD_COUNT)
    save_to_json_file(dummy_data, OUTPUT_FILE)
