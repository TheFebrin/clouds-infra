import db_read

class TestDBRead:

    def test_db_read(self):
        new_nick = db_read.create_new_nick({'nick': 'abc', 'name': 'test'})
        assert len(new_nick) == 7