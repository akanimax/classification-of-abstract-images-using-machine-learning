--@@ Coded by akmyths @@--
PS.
Few path changes made to the original codes to accommodate the changes

The Models folder should contain all the saved models (While committing I am removing them
since I am on a terrible internet service)
Files which should be present
checkpoint
classes.npy
DnnClassifier.h5
label_mappings.pickle
mod_1.ckpt.data-00000-of-00001
mod_1.ckpt.index
mod_1.ckpt.meta

Till now we have been working on the dataset as a whole dividing it programmatically.
While this is the way to go, the external might ask us which image are you entering as input
and we couldn't tell it apart from train and test.
So I have thought of segregating the images physically here into folders named by STYLES in the Media folder.
This code is working on a very small subset of the whole dataset (2-3 images per class)
We have to execute this code on lab PC for obvious reasons (RAW computing power)

While using the ensemble.csv we have to shuffle it.
Using command $shuf

Finally, it gives me immense pleasure to conclude our project
~Ameeth Kanawaday


