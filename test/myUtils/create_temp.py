import os
import tempfile
import shutil


def create_temp_file(size, content=None):
    f = tempfile.NamedTemporaryFile(delete=False)
    if content is None:
        content = b'\0' * size
    f.write(content)
    f.flush()
    return f


def create_temp_folder(files=None):
    temp_dir = tempfile.TemporaryDirectory()
    if files:
        for file in files:
            file_name = os.path.basename(file)
            new_file_path = os.path.join(temp_dir.name, file_name)
            shutil.move(file, new_file_path)

    value = [temp_dir, files]

    return value
