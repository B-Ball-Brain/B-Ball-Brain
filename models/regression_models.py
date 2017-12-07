from sklearn import linear_model
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import ExtraTreesRegressor

def linear_reg(data,label):
	reg = linear_model.LinearRegression()
	reg.fit(data,label)
	return reg

def ridge_regCV(data,label):
	reg = linear_model.RidgeCV(alphas=[0.1,1.0,10.0])
	reg.fit(data,label)
	return reg

def lasso_regCV(data,label):
	reg = linear_model.LassoCV(alphas=[0.1,1.0,10.0])
	reg.fit(data,label)
	return reg

def elastic_net_regCV(data,label):
	reg = linear_model.ElasticNetCV(alphas=[0.1,1.0,10.0])
	reg.fit(data,label)
	return reg

def bayesian_ridge_reg(data,label):
	reg = linear_model.BayesianRidge()
	reg.fit(data,label)
	return reg

def support_vector_reg(data,label):
	reg = SVR()
	reg.fit(data,label)
	return reg

def random_forrest_reg(data,label):
	reg = RandomForestRegressor(n_estimators=100)
	reg.fit(data,label)
	return reg

def gradient_boosting_reg(data,label):
	reg = GradientBoostingRegressor(n_estimators=100)
	reg.fit(data,label)
	return reg

def ada_boost_reg(data,label):
	reg = AdaBoostRegressor(n_estimators=100)
	reg.fit(data,label)
	return reg

def extra_trees_reg(data,label):
	reg = ExtraTreesRegressor(n_estimators=100)
	reg.fit(data,label)
	return reg