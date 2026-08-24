import baostock as bs


class BaostockClient:


    def __enter__(self):

        bs.login()

        return bs


    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb
    ):

        bs.logout()