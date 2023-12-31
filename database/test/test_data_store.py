from database import DataStore, Parameter


def test_initialize():
    data_store = DataStore()
    assert data_store.get(Parameter.INITIALIZED)


def test_get_method():
    data_store = DataStore()
    assert type(data_store.get(Parameter.INITIALIZED)) == bool
    assert type(data_store.get(Parameter.SPEED)) == float
    assert type(data_store.get(Parameter.GEAR)) == int


def test_set_method():
    data_store = DataStore()
    data_store.set(Parameter.TOW_MODE_LOCK, True)
    assert data_store.get(Parameter.TOW_MODE_LOCK) == True
    data_store.set(Parameter.SPEED, 123.321)
    assert data_store.get(Parameter.SPEED) == 123.321
    data_store.set(Parameter.GEAR, 2)
    assert data_store.get(Parameter.GEAR) == 2
