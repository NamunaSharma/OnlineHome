import pandas as pd
from myApp.models import Category, Service
from django.core.exceptions import ObjectDoesNotExist

# Read CSV file into a DataFrame
csv_file_path = r'C:\Users\Namuna Sharma\OneDrive\Desktop\HomeServices\onlineHome\myApp\servicesdataset.csv'  # Update with your actual CSV file path
df = pd.read_csv(csv_file_path)

# Iterate through the DataFrame and create model instances
for index, row in df.iterrows():
    try:
        # Get the category instance based on Category_id
        category_id = int(row['Category_id'])
        category_instance = Category.objects.get(id=category_id)

        # Parse dates in the correct format (you may need to format this based on your database format)
        created_at = pd.to_datetime(row['Created_At'], format='%d/%m/%Y %H:%M')
        updated_at = pd.to_datetime(row['Updated_At'], format='%d/%m/%Y %H:%M')

        # Create the Service instance
        service = Service(
            category=category_instance,  # Use the category instance
            title=row['Title'],  # Title from CSV
            description=row['Description'],  # Description from CSV
            price=row['Price'],  # Price from CSV
            image=row['Image_URL'],  # Image URL from CSV
            created_at=created_at,  # Created At from CSV
            updated_at=updated_at  # Updated At from CSV
        )

        # Save the service instance
        service.save()
        print(f"Service '{service.title}' has been created.")

    except Category.DoesNotExist:
        print(f"Category with ID {category_id} does not exist.")
    except KeyError as e:
        print(f"Missing column in CSV for index {index}: {e}")
    except Exception as e:
        print(f"Error processing row {index}: {e}")

print("CSV data has been loaded into the Django database.")
