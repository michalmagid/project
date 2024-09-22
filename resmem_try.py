import os
from PIL import Image
import torch
import pandas as pd
from resmem import transformer, ResMem
from openpyxl import Workbook

# Initialize the ResMem model
model = ResMem(pretrained=True)
# Set the model to inference mode.
model.eval()

# Specify the directory containing the images
image_dir = 'food _pics _non _food _pics'
# 'path/to/your/image/directory'

# Get a list of all image file names in the directory
image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png')]

# Create a new workbook
wb = Workbook()

# Create a worksheet in the workbook
ws = wb.active

# Set the initial row number
row_num = 1

# Initialize an empty list to store predictions
all_predictions = []

# Preprocess each image and stack them to form a batch
for image_file in image_files:
    img = Image.open(image_file).convert('RGB')
    file_name = os.path.basename(image_file)
    img_x = transformer(img)
    predictions = model(img_x.view(-1, 3, 227, 227))
    
    # Apply softmax to convert scores into probabilities
    probabilities = torch.softmax(predictions, dim=1)
    
    # Append probabilities to the list
    all_predictions.append(probabilities.detach().numpy())

    # Write the file name to the Excel file
    ws.cell(row=row_num, column=1, value=file_name)
    row_num += 1

# Convert probabilities list to a DataFrame
predictions_df = pd.DataFrame(all_predictions[0], columns=[f"Class_{i}" for i in range(probabilities.shape[1])])

# Save the DataFrame to an Excel file
predictions_df.to_excel('output_grey_rebbeca_softmax.xlsx', index=False)

print("Predictions (softmax probabilities) saved to 'output_grey_rebbeca_softmax.xlsx'")
