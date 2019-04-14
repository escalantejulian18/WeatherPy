# -*- coding: utf-8 -*-
import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Classifier
import weka.core.converters as converters
from weka.classifiers import Evaluation
from weka.core.classes import Random

# Iniciamos la maquina virtual de java
jvm.start()

# Obtenemos los datos
data_dir = "data.arff"
data = converters.load_any_file(data_dir)
data.class_is_last()

# Creamos el clasificador
cls = Classifier(classname="weka.classifiers.trees.J48", options = [ "-C" ,  "0.25", "-M", "2"])
cls.build_classifier(data)

# Evaluación del modelo
evl = Evaluation(data)
evl.crossvalidate_model(cls, data, 10, Random(1))


# Mostramos los resultados
print(evl.summary())
print(evl.class_details())
print(evl.matrix())