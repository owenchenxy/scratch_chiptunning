import pandas as pd

class CsvWriter(object):
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.has_header = False
        self.write_header = True
        self.mode = 'w'

    def write_to_csv(self, data_dict):
        #if os.path.exists(self.csv_file):
        #    print("Waring: File exists, skip writing {0}".format(self.csv_file))
        #    return
        DataFrame = pd.DataFrame(data_dict)
        DataFrame.to_csv(self.csv_file, mode=self.mode, index=False, header=self.write_header, sep=",")
        if not self.has_header:
            self.has_header = True
            self.write_header = False
            self.mode = 'a'

    def sort_csv(self):
        data = pd.read_csv(self.csv_file)
        data.sort_values(by='model', ascending=True, inplace=True)
        data.to_csv(self.csv_file, index=False)
        print("sorted %s" % self.csv_file)
