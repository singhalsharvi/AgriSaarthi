import os
import hashlib
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from sklearn.model_selection import train_test_split

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
RANDOM_SEED = 42

def compute_md5(file_path):
    """Compute MD5 hash of image content to detect duplicate images."""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None

def load_and_clean_dataset(data_dir="PlantDoc-Dataset", val_split=0.15):
    """
    Scans train and test directories in PlantDoc-Dataset.
    Removes data leakage between train and test splits by MD5 content hashing.
    Splits train images into train and validation sets (stratified).
    Returns (train_filepaths, train_labels), (val_filepaths, val_labels), (test_filepaths, test_labels), class_names, class_to_idx
    """
    train_dir = os.path.join(data_dir, "train")
    test_dir = os.path.join(data_dir, "test")

    if not os.path.exists(train_dir) or not os.path.exists(test_dir):
        raise FileNotFoundError(f"Dataset folders 'train' or 'test' not found under {data_dir}")

    train_classes = sorted([d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))])
    test_classes = sorted([d for d in os.listdir(test_dir) if os.path.isdir(os.path.join(test_dir, d))])
    
    all_classes = sorted(list(set(train_classes + test_classes)))
    class_to_idx = {c: i for i, c in enumerate(all_classes)}
    
    print(f"[Dataset] Identified {len(all_classes)} total agricultural disease classes.")

    raw_train_paths, raw_train_labels, train_hashes = [], [], {}
    for c in train_classes:
        c_path = os.path.join(train_dir, c)
        for f in os.listdir(c_path):
            fp = os.path.join(c_path, f)
            if os.path.isfile(fp) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp')):
                h = compute_md5(fp)
                if h:
                    train_hashes[h] = fp
                    raw_train_paths.append(fp)
                    raw_train_labels.append(class_to_idx[c])

    raw_test_paths, raw_test_labels = [], []
    leaked_count = 0
    for c in test_classes:
        c_path = os.path.join(test_dir, c)
        for f in os.listdir(c_path):
            fp = os.path.join(c_path, f)
            if os.path.isfile(fp) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp')):
                h = compute_md5(fp)
                if h and h in train_hashes:
                    leaked_count += 1
                    continue
                raw_test_paths.append(fp)
                raw_test_labels.append(class_to_idx[c])

    print(f"[Data Leakage Prevention] Purged {leaked_count} duplicate test images matching training set content.")

    train_paths, val_paths, train_labels, val_labels = train_test_split(
        raw_train_paths,
        raw_train_labels,
        test_size=val_split,
        stratify=raw_train_labels,
        random_state=RANDOM_SEED
    )

    print(f"[Dataset Summary] Train samples: {len(train_paths)}, Val samples: {len(val_paths)}, Test samples: {len(raw_test_paths)}")
    
    return (
        (train_paths, np.array(train_labels)),
        (val_paths, np.array(val_labels)),
        (raw_test_paths, np.array(raw_test_labels)),
        all_classes,
        class_to_idx
    )

class PlantDataset(Dataset):
    """PyTorch Dataset with Torchvision augmentation transformations."""
    def __init__(self, filepaths, labels, transform=None):
        self.filepaths = filepaths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.filepaths)

    def __getitem__(self, idx):
        fp = self.filepaths[idx]
        label = self.labels[idx]
        try:
            image = Image.open(fp).convert("RGB")
        except Exception:
            # Fallback black image if corrupt
            image = Image.new("RGB", IMG_SIZE, (0, 0, 0))
            
        if self.transform:
            image = self.transform(image)
        return image, label

def get_transforms(is_training=False):
    """Returns torchvision image preprocessing and augmentation transforms."""
    if is_training:
        return transforms.Compose([
            transforms.Resize(IMG_SIZE),
            transforms.RandomRotation(20),
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    else:
        return transforms.Compose([
            transforms.Resize(IMG_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

def build_data_loaders(train_data, val_data, test_data, batch_size=BATCH_SIZE):
    """Builds PyTorch DataLoaders for train, val, and test splits."""
    train_ds = PlantDataset(train_data[0], train_data[1], transform=get_transforms(is_training=True))
    val_ds = PlantDataset(val_data[0], val_data[1], transform=get_transforms(is_training=False))
    test_ds = PlantDataset(test_data[0], test_data[1], transform=get_transforms(is_training=False))

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False, num_workers=0)

    return train_loader, val_loader, test_loader
