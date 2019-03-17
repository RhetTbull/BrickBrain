from imageai.Prediction.Custom import CustomImagePrediction
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

execution_path = os.getcwd()

prediction = CustomImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath("/Users/rhet/Dropbox/code/scifair/lego/models/model_ex-023_acc-0.902638.h5")
prediction.setJsonPath("/Users/rhet/Dropbox/code/scifair/lego/json/model_class.json")
prediction.loadModel(num_objects=16)

predictions, probabilities = prediction.predictImage("/Users/rhet/Dropbox/code/scifair/missing-pieces.jpg", result_count=5)

for eachPrediction, eachProbability in zip(predictions, probabilities):
    print(eachPrediction , " : " , eachProbability)