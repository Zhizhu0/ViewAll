import json
import os.path

from ViewAll.view_all_core import ViewAllShow, base_path


class ViewAllShowMain(ViewAllShow):
    def __init__(self):
        super().__init__()
        self.set_title('main')


if __name__ == '__main__':
    ViewAllShowMain().run()


