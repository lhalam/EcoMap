class TestData:
    def __init__(self, file_path):
        self.file_path = file_path

    def get(self, keyword):
        test_data = ""
        with open(self.file_path, 'r') as f:
            for line in f:
                index = line.find(keyword + ":")
                if index != -1:
                    test_data = line[(index + len(keyword) + 1):]
                    break
        return test_data.strip()
