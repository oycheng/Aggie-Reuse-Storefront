import barcode

# Generate a random EAN-13 barcode number
import random

random.seed()  # Initialize random number generator
barcode_number = ''.join(str(random.randint(0, 9)) for _ in range(9))

# Create the barcode SVG
ean = barcode.get_barcode_class('ean13')
ean_barcode = ean(barcode_number)

# Save the barcode SVG to a file
barcode_filename = "barcode_" + barcode_number
ean_barcode.save(barcode_filename)
print(f"Generated barcode with number: {barcode_number}")
print(f"Barcode SVG saved as: {barcode_filename}")

