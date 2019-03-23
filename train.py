import turicreate as tc
import os.path

photo_folder = 'kaggle'

# Load images (Note: you can ignore 'Not a JPEG file' errors)
print("loading images")
data = tc.image_analysis.load_images(photo_folder, with_path=True)

# From the path-name, create a label column
print("adding names")
data['label'] = data['path'].apply(lambda path: os.path.basename(os.path.dirname(path)))

print("creating training data and testing data")
train_data, test_data = data.random_split(0.8)

print("saving data frames")
# Save the data for future use
train_data.save(photo_folder+'.sframe')

# # Load images (Note: you can ignore 'Not a JPEG file' errors)
# test_data = tc.image_analysis.load_images('lego/test', with_path=True)

# From the path-name, create a label column
# test_data['label'] = test_data['path'].apply(lambda path: os.path.basename(os.path.dirname(path)))

# Save the data for future use
test_data.save(photo_folder+'.sframe')

print("classifying")
model = tc.image_classifier.create(train_data, target='label', max_iterations=100)

print("creating predications")
# Save predictions to an SArray
predictions = model.predict(test_data)

# Evaluate the model and save the results into a dictionary
metrics = model.evaluate(test_data)
print(metrics['accuracy'])

print("saving model")
# Save the model for later use in Turi Create
model.save(photo_folder+'.model')

# Export for use in Core ML
model.export_coreml('MyCustomImageClassifier_'+photo_folder+'.mlmodel')




