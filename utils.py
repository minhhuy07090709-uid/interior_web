import cloudinary.uploader
def save_image(file):
    if not file or not file.filename:
        return None
    try:
        result= cloudinary.uploader.upload(file,folder='interior_web')
        return result['secure_url']
    except Exception as e:
        print('Upload error:',e)
        return None