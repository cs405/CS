import uuid
import hashlib
import random
import json


class PayForUse:
    def get_machine_code(self):
        # Get the machine's unique ID
        machine_code = uuid.getnode()
        return machine_code

    def generate_charge_code(self, machine_code):
        # Convert the machine code to a string
        machine_code_str = str(machine_code)
        # Hash the machine code
        hashed_machine_code = hashlib.sha256(machine_code_str.encode()).hexdigest()
        # Convert some characters to uppercase
        modified_hash = ''.join(c.upper() if random.Random(machine_code + i).random() < 0.5 else c for i, c in enumerate(hashed_machine_code))
        # Take the first 50 characters as the charge code
        charge_code = modified_hash[:50]
        return charge_code

    @staticmethod
    def load_json(path):
        with open(path, 'r') as f:
            json_file = json.loads(f.read())
        return json_file

    @staticmethod
    def save_json(jsonfile):
        with open('./constants.json', 'w') as f:
            f.write(json.dumps(jsonfile))


    def is_pay(self,path):
        json_file = self.load_json(path)
        if json_file['validate_num'] == self.generate_charge_code(json_file['machine_num']):
            return True
        else:
            return False

# print(PayForUse().generate_charge_code(228939412275842))