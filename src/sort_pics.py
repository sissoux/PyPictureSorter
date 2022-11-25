import pathlib
import hashlib
import os
from PIL import Image


class PictureSorter:
    """PictureSorter class
    """
    def __init__(self, path: pathlib.Path) -> None:
        self.path = path
        self.date_taken = Image.open(path)._getexif()[36867]
        with open(path, mode="rb") as f:
            img_data = f.read()
            self.hash = hashlib.md5(img_data)
        self.new_path = None

    def get_new_name(self, move_to_path=None):
        return pathlib.Path().joinpath(
            self.path.parent if move_to_path is None else move_to_path,
            f"{self.date_taken.replace(':','_').replace(' ','_')}{self.path.suffix}",
        )

    def rename(self, destination=None):
        """Rename current file based on date taken, move it to new location if move_to_path is provided"""
        self.new_path = self.get_new_name(destination)
        if not destination.exists():
            destination.mkdir(parents=True, exist_ok=True)
        os.rename(self.path, self.new_path)
    
    def __hash__(self):
        return int(self.hash.hexdigest(), 16)
    
    def __eq__(self, other:object) -> bool:
        return isinstance(other,PictureSorter) and self.hash.digest() == other.hash.digest()


input_path = pathlib.Path("Pictures")
output_path = pathlib.Path("Output")

input_file_pathes = list(input_path.glob("**/*.*"))

images = {PictureSorter(x) for x in input_file_pathes}

print(f"Found {len(images)} pictures, {len(images)-len(input_file_pathes)} duplicates." )

for img in images:
    img.rename(output_path)
    print(
        f"Pic {img.path.name} taken on {img.date_taken} hash is {img.hash.hexdigest()} will be renamed as {img.new_path}"
    )
