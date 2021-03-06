<<<<<<< HEAD
#Centering and scaling
def fun_scaling_data():
    #standarization: substract the mean and divide by variance
    #all features are centered around zero and have variance one
    #can also subtract the minimum and divide by the range
    #minimun zero an maximum one
    # Import scale
    from sklearn.preprocessing import scale

    # Scale the features: X_scaled
    X_scaled = scale(X)

    # Print the mean and standard deviation of the unscaled features
    print("Mean of Unscaled Features: {}".format(np.mean(X))) 
    print("Standard Deviation of Unscaled Features: {}".format(np.std(X)))

    # Print the mean and standard deviation of the scaled features
    print("Mean of Scaled Features: {}".format(np.mean(X_scaled))) 
    print("Standard Deviation of Scaled Features: {}".format(np.std(X_scaled)))


def fun_scaling_pipeline():
    # Import the necessary modules
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline

    # Setup the pipeline steps: steps
    steps = [('scaler', StandardScaler()),
            ('knn', KNeighborsClassifier())]
            
    # Create the pipeline: pipeline
    pipeline = Pipeline(steps)

    # Create train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3, random_state=42)

    # Fit the pipeline to the training set: knn_scaled
    knn_scaled = pipeline.fit(X_train,y_train)

    # Instantiate and fit a k-NN classifier to the unscaled data
    knn_unscaled = KNeighborsClassifier().fit(X_train, y_train)

    # Compute and print metrics
    print('Accuracy with Scaling: {}'.format(knn_scaled.score(X_test,y_test)))
    print('Accuracy without Scaling: {}'.format(knn_unscaled.score(X_test,y_test)))
=======
def fun_myfirstpipeline():
    # Import the Imputer module
    from sklearn.preprocessing import Imputer
    from sklearn.svm import SVC

    # Setup the Imputation transformer: imp
    imp = Imputer(missing_values='NaN', strategy='most_frequent', axis=0)

    # Instantiate the SVC classifier: clf
    clf = SVC()

    # Setup the pipeline with the required steps: steps
    steps = [('imputation', imp),
            ('SVM', clf)]
>>>>>>> 745d093781587a948aab81d8f2da689834e84dda
