import torch
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
NUM_CLASSES = 2
CLASSES = ['_background_','Urdu']

