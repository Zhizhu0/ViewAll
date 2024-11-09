from view_all_core import ViewAllShow


class ViewAllShowMain(ViewAllShow):
    def __init__(self):
        super().__init__()
        # 设置大小
        self.resize(400, 300)
        self.set_title('main')


if __name__ == '__main__':
    ViewAllShowMain().run()
