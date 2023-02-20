
const liveData = {
  namespaced: true,
  state: {
    data1: 0,
    data2: "",
    data3: []
  },
  mutations: {
    setData1(state, value) {
      state.data1 = value
    },
    setData2(state, value) {
      state.data2 = value
    },
    setData3(state, value) {
      state.data3 = value
    }
  },
  actions: { }
}

export default liveData
