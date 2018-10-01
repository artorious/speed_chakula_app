import unittest


class TestDevConfig(unittest.TestCase):
    """ Tests Dvelopment configurations """
    def create_app(self):
        app.config.from_object('instance.config.DevConfig')
        return app
        