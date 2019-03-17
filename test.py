#test predictions from model we created

import turicreate as tc
import sys

image = sys.argv[1]

# Load the data
data = tc.image_analysis.load_images(image, with_path=True)

# Create the model
model = tc.load_model('legopics.model')

# Save predictions to an SArray
predictions = model.classify(data)
#predictions.print_rows(num_rows=17)

for i in range(len(data)):
    print(data[i]['path'],", ", predictions[i]['class'], ", ", "{0:.0f}%".format(predictions[i]['probability']* 100), " confidence")
