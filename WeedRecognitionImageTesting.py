from imageai.Prediction.Custom import CustomImagePrediction
import os
import datetime

execution_path = os.getcwd()

prediction = CustomImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath("resnet.hdf5")
prediction.setJsonPath("weeds_model_class.json")
print("loading model")
start=datetime.datetime.now()
prediction.loadModel(num_objects=9)
end=datetime.datetime.now()
delta=end-start
print(str(delta))

images =["lawn0_grass.jpg", "lawn1_Chinee_apple.jpg"]
for image in images:
    print("processing image:" + image)
    startImgDetection=datetime.datetime.now()
    predictions, probabilities = prediction.predictImage(image, result_count=3)
    endImgDetection=datetime.datetime.now()
    imgDetectionDelta=endImgDetection-startImgDetection
    print(str(imgDetectionDelta))
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        print(eachPrediction , " : " , eachProbability)
