from django.test import TestCase

# Create your tests here.
import pandas as pd

df = pd.read_csv("sign_data.csv")
print(df["label"].value_counts())  # Count all unique labels
