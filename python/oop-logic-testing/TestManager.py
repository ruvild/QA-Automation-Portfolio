import json
import os


class TestManager:
    def __init__(self, filename):
        self.filename = filename
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.file_list = json.load(f)
        else:
            self.file_list = []

    def add_result(self, test_name, status):
        self.test_data = dict(test_name=test_name, status=status)
        self.file_list.append(self.test_data)

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.file_list, f, indent=4)

    def get_passed(self):
        return [
            test['test_name'] for test in self.file_list if test['status'] == 'Pass'
        ]

    def clear_results(self):
        self.file_list = []
        self.save()
        print("Test history cleared.\n")


manager = TestManager("my_tests2.json")
manager.add_result("Login Test", "Pass")
manager.add_result("Checkout Test", "Fail")
manager.add_result("Checkout Test_2", "Pass")
manager.add_result("Logout Test", "Fail")
manager.save()

print(manager.get_passed())

# manager.clear_results()
