# USE %timeit in ipython to see how long it takes.


import libraries
#is a rule for calculating an estimate of a given queantify based on observed data
#In scikit-learn, an stimator for classification is a Python object that implements the methods fit(X,y) and predict(T)

#fit, usually TRAINING, takes some samples X, targets y if the model is supervised, and potencially sample_weight, it should estimate an sotre model sttributes
#fit_predict, Used for unsupervised, transductive estimator, fits a model an return predictions, they are store in labels_is, .fit(X).predict(X)
#fit_transform, transforms which fits and returns transformed training data, to float64
#transforn, transform fit(X), ouput is an array or sparce matrix
#predict, PREDICT WHICH LABEL WILL BE THE DATA
class Model:
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

    def knn(self):
        # Import necessary modules
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.model_selection import train_test_split

        digits =datasets.load_digits()
        # Create feature and target arrays
        X = digits.data
        y = digits.target

        # Split into training and test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42, stratify=y)

        # Create a k-NN classifier with 7 neighbors: knn
        knn = KNeighborsClassifier(n_neighbors=7)

        # Fit the classifier to the training data
        knn.fit(X_train, y_train)

        # Print the accuracy
        print(knn.score(X_test, y_test))

        ###########################################
        # scores data entranada vs data test
        ############################################
        # Setup arrays to store train and test accuracies
        neighbors = np.arange(1, 9)
        train_accuracy = np.empty(len(neighbors))
        test_accuracy = np.empty(len(neighbors))

        # Loop over different values of k
        for i, k in enumerate(neighbors):
            # Setup a k-NN Classifier with k neighbors: knn
            knn = KNeighborsClassifier(n_neighbors=k)

            # Fit the classifier to the training data
            knn.fit(X_train, y_train)
            
            #Compute accuracy on the training set
            train_accuracy[i] = knn.score(X_train,y_train )

            #Compute accuracy on the testing set
            test_accuracy[i] = knn.score(X_test, y_test)

        # Generate plot
        plt.title('k-NN: Varying Number of Neighbors')
        plt.plot(neighbors, test_accuracy, label = 'Testing Accuracy')
        plt.plot(neighbors, train_accuracy, label = 'Training Accuracy')
        plt.legend()
        plt.xlabel('Number of Neighbors')
        plt.ylabel('Accuracy')
        plt.show()
    def lineal_regression():
        #boston housing data
        #gapminder.csv
        # for quantitative targets
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)

        reg_all =LinearRegresion()
        reg_all.fit(X_train, y_train)
        y_pred = reg_all.predict(X_test)


        #precicion del model accuracy R2
        reg_all.score(X_test,y_test)
        # Error loss function it could be
        np.sqrt(mean_squared_error(y_test,y_pred))
        pass

        ###
        #CROS VALIDATION

        cv_results = cross_val_score(reg,X,y,cv=5) # 5 muestras de la data

    ####REGULARIZE regression
    def ridge_regression():
        
        #recall linear regression minimizes a loss function
        # it chooses a coefficient for each feature variable
        #large coefficients can lead to overfitting

        #TYPES
        #ridge regression (needs picking alpha  -> is like pikcing K IN KNN)
        from sklearn.linear_model import Ridge 
        ridge = Ridge(alpha=0.1,normalizae= True)
        ridge.fit(X_train,y_train)
        ridge_predict(X_test)
        ridge.score(X_test,y_test)

    #can be used to select important features of a dataset
    def lasso_regression():
        from sklearn.linear_model import Lasso 
        lasso = Lasso(alpha=0.1,normalize= True)
        lasso.fit(X_train,y_train)
        lasso_predict(X_test)
        lasso.score(X_test,y_test)

        print(lasso.coef_) # coeficientes show
        #plot coefficients
        plt.plot(range(len(df_columns)), lasso_coef)
        plt.xticks(range(len(df_columns)), df_columns.values, rotation=60)
        plt.margins(0.02)
        plt.show()


    
    # loss_function, calcule distance between result and target
    # general use for linear regresion
    def loss_function():
        pass
    # separa la data entrenamiento y prediccion 
    def cross_validation():
        pass

def display_plot(cv_scores, cv_scores_std):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(alpha_space, cv_scores)

    std_error = cv_scores_std / np.sqrt(10)

    ax.fill_between(alpha_space, cv_scores + std_error, cv_scores - std_error, alpha=0.2)
    ax.set_ylabel('CV Score +/- Std Error')
    ax.set_xlabel('Alpha')
    ax.axhline(np.max(cv_scores), linestyle='--', color='.5')
    ax.set_xlim([alpha_space[0], alpha_space[-1]])
    ax.set_xscale('log')
    plt.show()
class EvaluatingModel:
    def cross_validation():
        from sklearn.model_selection import cross_val_score
        #reg linear regresion model
        cv_results = cross_val_score(reg,X,y,cv=5) # 5 muestras de la data, devuelve 5 arrays




    # Import necessary modules
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score

# Setup the array of alphas and lists to store scores
alpha_space = np.logspace(-4, 0, 50)
ridge_scores = []
ridge_scores_std = []

# Create a ridge regressor: ridge
ridge = Ridge(normalize=True)

# Compute scores over range of alphas
for alpha in alpha_space:

    # Specify the alpha value to use: ridge.alpha
    ridge.alpha = alpha
    
    # Perform 10-fold CV: ridge_cv_scores
    ridge_cv_scores = cross_val_score(ridge, X,y, cv=10)
    
    # Append the mean of ridge_cv_scores to ridge_scores
    ridge_scores.append(np.mean(ridge_cv_scores))
    
    # Append the std of ridge_cv_scores to ridge_scores_std
    ridge_scores_std.append(np.std(ridge_cv_scores))

# Display the plot
display_plot(ridge_scores, ridge_scores_std)

