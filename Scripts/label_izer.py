from six.moves import cPickle as pickle
import os

'''Set the constant paths here'''
# set the paths required for the script to work:
root = "../Data/"
pickle_file_path = root + "Data_pindown.pickle"
log_path = root + "logs"
model_path = os.path.join(root, "Models/Model1/")


Formatted_Data = {}
with open(pickle_file_path, "rb") as f:
    Formatted_Data = pickle.load(f)

labels_mappings = Formatted_Data['label_mapping']
print(labels_mappings)


with open(os.path.join(root, "label_mappings.pickle"), "wb") as pickle_file:
    my_dict = pickle.dump(labels_mappings, pickle_file, pickle.HIGHEST_PROTOCOL)
