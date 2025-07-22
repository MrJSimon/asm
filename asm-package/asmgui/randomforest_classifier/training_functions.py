##############################################################################
# Author:      Jamie, Germano & Nikhil
#
# Description: This script builds a random forest decision tree model
#              utilizing the algorithms/tools from the sklearn library.
#              It can also use the model to predict features onto other images.
#
# References:  https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.
# RandomForestClassifier.html
##############################################################################
"""RandomForest classifier to classify images"""
# Import packages
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import numpy as np
from asmgui.randomforest_classifier.feature_space import feature_extraction
import matplotlib.pyplot as plt

def print_accuracy(model_i, xtrain_i, xtest_i, ytrain_i, ytest_i):
    '''
    Print the percentage prediction between predicted, test & train.

    Args:
        model_i: Fitted RandomForestClassifier model
        xtrain_i: Dataframe containing percentage of total amount of
                 feature data
        xtest_i: Dataframe containing percentage of total amount of
                feature data
        ytrain_i: Vector containing percentage of reshaped masked image 
        ytest_i: Vector containing percentage of reshaped masked image
    '''
    # Make prediction on training data
    prediction_test_train = model_i.predict(xtrain_i)
    # Make prediction on test data
    prediction_test = model_i.predict(xtest_i)
    print ("Accuracy on training data = ", metrics.accuracy_score(ytrain_i, prediction_test_train))    
    print ("Accuracy on test data = ", metrics.accuracy_score(ytest_i, prediction_test))

def train_random_forest(img_mi, img_fi, features_i, nest=10):
    '''
    Train a random forest model between the mask and image using features
    from feature_extraction.

    Args:
        img_mi: Masked image
        img_fi: Original image
        nest: Number of decision trees (default=10)

    Returns:
        model: The fitted model
    '''
    x = feature_extraction(img_fi,features_i) 
    # Define the dependent variable that needs to be predicted (labels)
    # we reshape it into a single vector. This has to be done, otherwise
    # the sklearn functions will not work.
    y = img_mi.reshape(-1)
    # Get all position to where the vector is non-zero meaning we are ignoring
    # values which have labels that are zero and vice-versa
    nonzero_ind = np.argwhere(y).reshape(-1).tolist()
    # Set new y and x
    x,y = x.iloc[nonzero_ind], y[nonzero_ind]
    # Create test and training data, with a 40% split - random state is kept constant
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=20)
    # Build model - Random forrest with 10 desecision trees, random state is kept constant
    model = RandomForestClassifier(n_estimators = nest, random_state = 42)
    # Fit the model to the data
    model.fit(x_train, y_train)
    # Print accuracy
    print_accuracy(model,x_train,x_test,y_train,y_test)
    # Return the model
    return model

def predict_features(model_i, img_fi, features_i):
    '''
    Predict features using a fitted RandomForestClassifier model.

    Args:
        model_i: Fitted RandomForestClassifier model.
        img_fi: Original image

    Returns:
        segmented: Segmented image
    '''
    # Get features to which the random forest shall be trained
    x = feature_extraction(img_fi, features_i)
    # Get resulting output
    result = model_i.predict(x)
    # Segment image
    segmented = result.reshape((img_fi.shape))
    return segmented
