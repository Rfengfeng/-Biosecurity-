from PIL import Image

# def image_type(image_file):
#     image_data = image_file
#     image_format = 'jpeg'  # 默认格式
#     if image_data.startswith(b'\xFF\xD8'):
#         image_format = 'jpeg'
#     elif image_data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
#         image_format = 'png'
#     elif image_data.startswith(b'\x47\x49\x46\x38\x39\x61') or image_data.startswith(b'\x47\x49\x46\x38\x37\x61'):
#         image_format = 'gif'
#     elif image_data.startswith(b'\x42\x4D'):
#         image_format = 'bmp'
#     elif image_data.startswith(b'\x00\x00\x01\x00'):
#         image_format = 'ico'
#     elif image_data.startswith(b'\x00\x00\x02\x00'):
#         image_format = 'cur'
#     elif image_data.startswith(b'\x00\x00\x00\x0C'):
#         image_format = 'ico'
#     elif image_data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
#         image_format = 'png'
#     elif image_data.startswith(b'\x4D\x4D\x00\x2A') or image_data.startswith(b'\x49\x49\x2A\x00'):
#         image_format = 'tiff'
#     # 根据图像格式设置正确的 MIME 类型
#     if image_format == 'jpeg':
#         mime_type = 'image/jpeg'
#     elif image_format == 'png':
#         mime_type = 'image/png'
#     elif image_format == 'gif':
#         mime_type = 'image/gif'
#     elif image_format == 'bmp':
#         mime_type = 'image/bmp'
#     elif image_format == 'ico':
#         mime_type = 'image/x-icon'
#     elif image_format == 'cur':
#         mime_type = 'image/vnd.microsoft.icon'
#     elif image_format == 'tiff':
#         mime_type = 'image/tiff'
#     else:
#         mime_type = 'application/octet-stream'  # 默认 MIME 类型
#     return(mime_type)

def image_type(image_file):
    # Convert file object to image object
    img = Image.open(image_file)    
    # Check if the image format is JPEG
    if img.format == 'JPEG':
       return(True)
    return(False)