import pandas as pd
import os

class CsvWriter(object):
    def __init__(self, base_dir):
        if base_dir[-1] == '/':
            base_dir = base_dir[:-1]
        self.base_dir = base_dir
        self.mode = 'w'
        self.write_header = True

    def write_to_csv(self, data_dict):
        csv_file = "{0}/{1}.csv".format(self.base_dir, data_dict['brand'][0].replace(' ', '_'))
        if os.path.exists(csv_file):
            self.write_header = False
            self.mode = 'a'
        else:
            self.write_header = True
            self.mode = 'w'
        try:
            DataFrame = pd.DataFrame(data_dict)
            DataFrame.to_csv(csv_file, mode=self.mode, index=False, header=self.write_header, sep=",")
        except Exception:
            print("Data invalid")
            print(data_dict)

    def sort_csv(self):
        count = 0
        for f in os.listdir(self.base_dir):
            if f[-4:] != ".csv":
                continue
            count += 1
            f = "{0}/{1}".format(self.base_dir, f)
            data = pd.read_csv(f)
            data.sort_values(by='model', ascending=True, inplace=True)
            data.to_csv(f, index=False)
            print("sorted %s" % f)
