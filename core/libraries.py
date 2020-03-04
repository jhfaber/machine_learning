from sklearn import datasets
from sklearn import svm

# VISUALISATION
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


import numpy as np
from sklearn import random_projection



###############################
# VOCABULARY
# clf classifier
# https://scikit-learn.org/stable/glossary.html#glossary





###########################
# LIBRARIES CLASS
# datasets are dicts that containts data and some metadata
############################333
# data where are store all the data
# target response variables 
# feature_names, names of each data column 
class ExternalDatasets:

    def get_iris(self,re_x_y=False):
        #return_X_y=re_x_y return data and target
        self.iris  = datasets.load_iris(return_X_y=re_x_y)

        return self.iris

    #TO PREDICT, giving an image, which digit it represent
    def get_digits(self):
        self.digits =datasets.load_digits()
        return self.digits 
    def show_img_digits(self,x):
        plt.figure(1, figsize=(3, 3))
        plt.imshow(self.digits.images[x], cmap=plt.cm.gray_r, interpolation='nearest')
        plt.show()


#is a rule for calculating an estimate of a given queantify based on observed data
#In scikit-learn, an stimator for classification is a Python object that implements the methods fit(X,y) and predict(T)

#fit, usually TRAINING, takes some samples X, targets y if the model is supervised, and potencially sample_weight, it should estimate an sotre model sttributes
#fit_predict, Used for unsupervised, transductive estimator, fits a model an return predictions, they are store in labels_is, .fit(X).predict(X)
#fit_transform, transforms which fits and returns transformed training data, to float64
#transforn, transform fit(X), ouput is an array or sparce matrix
#predict, PREDICT WHICH LABEL WILL BE THE DATA

class Estimator:
    # CLASIFICATION 

    def ciclo(self):
        #primero se entrena con fit(X,y) X la muestra y y los target
        #Luego se predice predict 
        pass
    # methods fit, predict

    # FIT RECEIBE DATA AN TARGET
    def support_vector_classification(self):
        # EXAMPLE USE
        # clf.fit(digits.data[:-1],digits.target[:-1])   FIT, receive 2 arrays In statistics, a fit refers to how well you approximate a target function
        # clf.predict(digits.data[-1:])  receive data
        self.clf = svm.SVC(gamma=0.001, C=100.)
        return self.clf



# https://scikit-learn.org/stable/modules/model_evaluation.html
# EVALUATION MODEL



class ModelEvaluation:
    # y_true1d array-like, or label indicator array / sparse matrix
    # Ground truth (correct) target values.

    # y_pred1d array-like, or label indicator array / sparse matrix
    # Estimated targets as returned by a classifier.
    def classificationreport(self):
        pass



##################
# GUARDAR 
class ModelPersistence:

    def __init__():
        import pickle
        from joblib import dump, load
    # Save model using pickle
    def save_using_pickle(self, clf):
        s = pickle.dumps(clf)
        clf2 = pickle.loads(s)
        # clf2.predict(X[0:1])
        return clf2
    

    # saving in a file a retrieve
    def save_using_joblib(self, clf):
        dump(clf, 'filename.joblib') 

    def get_using_joblib(self,clf_name='filename'):
        clf = load(clf_name+'.joblib') 
        return clf


    
class randomDataGeneration:
    def randomSeed(self, seed=0, arr=[10,2000]):
        rng = np.random.RandomState(0)  # SEED, IT  DON'T ALLOW TO CHANGE
        X = rng.rand(arr[0], arr[1])          # random in a range
        X = np.array(X, dtype='float32')# transform everything to float32

        return X


class scaleReduction:


    def gaussianRandom(self, X):
        transformer = random_projection.GaussianRandomProjection()
        self.X_new = transformer.fit_transform(X)

        return self.X_new


class buildChart():
    #COMPARAR X, Y
    import matplotlib.pyplot as plt

    title=''
    label_x=''
    label_y=''

    yticks = [[],[] ] #cambiar nombres de los label en y, [0] originales [1] el reemplazo
    xticks = [[],[]]
    #xticks(tick_val,tick_lab)
    ###########################################
    # COLOR
    #####################################
    # c parameter color receive a dict 


    #################################3
    # ADD TEXT
    ##############################33
    #plt.text(23,3423,'China')


    def __init__(self, title='',label_x='',label_y=''):
        self.title=title
        self.label_x=label_x
        self.label_y=label_y

    # plt.show() #its show plot
    # plt.xscale('log') agrega scala logaritmica
    def hello(self):
        print("ey")

    def labelsAttributes(self):
        plt.xlabel(self.label_x)
        plt.ylabel(self.label_y)
        plt.title(self.title)
    
    def linearChart(self,arr_x,arr_y):
        plt.plot(arr_x,arr_y)
        self.labelsAttributes()


    #Cuando el line plot se satura
    # s scalar array (burbujas)
    def scatterChart(self, arr_x,arr_y,s=None):
        plt.scatter(arr_x,arr_y,s=s)
        self.labelsAttributes()

    #get idea about diistribution
    # bins number of columns
    def histogramChart(self,arr_x, bins=3):
        plt.hist(arr_x, bins=bins)
        self.labelsAttributes()






