from resmem import ResMem, transformer

model = ResMem(pretrained=True)

""" The `transformer` is designed to be used with pillow.

python"""
from PIL import Image

#img = Image.open(r'C:\Users\USER\Downloads\FoodCal\Pics\F03_BC_sal.jpg')

img = Image.open('photo path')

 # This loads your image into memory
img = img.convert('RGB') 
# This will convert your image into RGB, for instance if it's a PNG (RGBA) or if it's black and white.

model.eval()
# Set the model to inference mode.

image_x = transformer(img)
# Run the preprocessing function

prediction = model(image_x.view(-1, 3, 227, 227))
print(prediction)
# For a single image, the image must be reshaped into a batch
# with size 1.
# Get your prediction!
