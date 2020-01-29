from sklearn import datasets

class Libraries:
       

    def get_iris(self):
        self.iris = datasets.load_iris()
        return iris
    def get_datasets(self):
        self.datasets=datasets.load_digits()
        return datasets


