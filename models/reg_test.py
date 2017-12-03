import numpy as np
from sklearn.metrics import mean_squared_error
from regression_models import linear_reg, support_vector_reg, ridge_regCV, lasso_regCV, \
elastic_net_regCV, random_forrest_reg, gradient_boosting_reg, ada_boost_reg, extra_trees_reg, bayesian_ridge_reg
from load_data import load_data

def test_models(model,test_data, test_label):
	function = model
	print("The mean squared error on the test data is %0.2f" % mean_squared_error(test_label, function.predict(test_data)))

data = load_data()
train_data = data['train_data']
train_label = data['train_label']
test_data = data['test_data']
test_label = data['test_label']

print("Training on %s examples" % train_data.shape[0])
print("Testing on %s examples" % test_data.shape[0])

#Un-comment to train using a different model

#model = ridge_regCV(train_data,train_label)
#model = lasso_regCV(train_data,train_label)
#model = elastic_net_regCV(train_data,train_label)
model = bayesian_ridge_reg(train_data,train_label)
#model = support_vector_reg(train_data,train_label)
#model = gradient_boosting_reg(train_data,train_label)
#model = random_forrest_reg(train_data,train_label)
#model = linear_reg(train_data,train_label)
#model = ada_boost_reg(train_data,train_label)
#model = random_forrest_reg(train_data,train_label)
print("The mean squared error on the training data is %0.2f" % mean_squared_error(train_label, model.predict(train_data)))
test_models(model,test_data,test_label)
	