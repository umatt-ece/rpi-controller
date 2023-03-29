from database import DataStore, LiveData, StoredData


def test_initialize():
    data_store = DataStore()
    assert data_store.get(LiveData.INITIALIZED)
    assert data_store.get(StoredData.INITIALIZED)


def test_get_method():
    data_store = DataStore()
    assert type(data_store.get(LiveData.INITIALIZED)) == bool
    assert type(data_store.get(LiveData.SPEED)) == float
    assert type(data_store.get(LiveData.GEAR)) == int


def test_set_method():
    data_store = DataStore()
    data_store.set(LiveData.TOW_MODE_LOCK, True)
    assert data_store.get(LiveData.TOW_MODE_LOCK) == True
    data_store.set(LiveData.SPEED, 123.321)
    assert data_store.get(LiveData.SPEED) == 123.321
    data_store.set(LiveData.GEAR, 2)
    assert data_store.get(LiveData.GEAR) == 2
