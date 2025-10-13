from PIL import Image

# Paths
png_path = r"C:\Users\mbraun\Python\Automation\textsearch\textsearch\image.png"
ico_path = r"C:\Users\mbraun\Python\Automation\textsearch\textsearch\image.ico"

# Open the PNG and save as multi-resolution ICO
img = Image.open(png_path)
img.save(ico_path, format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])

print(f"✅ Created icon: {ico_path}")
