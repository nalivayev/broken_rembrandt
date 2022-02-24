from PIL import Image


class CheckerParser:

    pass


class CheckerLogger:

    pass


class Checker:

    def do(self, p_file_name: str):
        try:
            im = Image.load(p_file_name)
            im.verify()
            im.close()
            im = Image.load(p_file_name)
            im.transpose(Image.FLIP_LEFT_RIGHT)
            im.close()
        except Exception:
            pass
