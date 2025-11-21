from PIL import Image, ImageDraw

img = Image.new('RGB', (3000, 2000), color = 'red')
d = ImageDraw.Draw(img)
d.text((10,10), "Hello World", fill=(255,255,0))
img.save('test_image.jpg')
print("Created test_image.jpg")
