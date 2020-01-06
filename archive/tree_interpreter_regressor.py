from treeinterpreter import treeinterpreter as ti

prediction, bias, contributions = ti.predict(model, [X_test[0]])
print(prediction)
print(bias)
print(contributions)
