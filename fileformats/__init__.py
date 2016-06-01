import os


def get_metadata_handler(path):
    base, ext = os.path.splitext(path)
    ext = ext[1:].lower()

    from fileformats import jpeg, mov, avi
    if ext in ['jpg', 'jpeg']:
        fmtKlass = jpeg.JPEGFile
    elif ext in ['mov', 'mp4']:
        fmtKlass = mov.MOVFile
    elif ext == 'avi':
        fmtKlass = avi.AVIFile
    else:
        raise Exception("Unknown file extension: %s" % ext)
    return fmtKlass
