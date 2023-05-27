from database import DataStore, Parameters


def test_initialize():
    data_store = DataStore()
    assert data_store.get(Parameters.INITIALIZED)


def test_get_method():
    data_store = DataStore()
    assert type(data_store.get(Parameters.INITIALIZED)) == bool
    assert type(data_store.get(Parameters.SPEED)) == float
    assert type(data_store.get(Parameters.GEAR)) == int


def test_set_method():
    data_store = DataStore()
    data_store.set(Parameters.TOW_MODE_LOCK, True)
    assert data_store.get(Parameters.TOW_MODE_LOCK) == True
    data_store.set(Parameters.SPEED, 123.321)
    assert data_store.get(Parameters.SPEED) == 123.321
    data_store.set(Parameters.GEAR, 2)
    assert data_store.get(Parameters.GEAR) == 2
