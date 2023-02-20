import { createStore } from "vuex"

import liveData from "@/store/liveData"
import storedData from "@/store/storedData"

const store = createStore({
  modules: {
    liveData, storedData
  },
  state: {
    title: "Vuex Store",
    engineTemperature: 0.0,
    enginePower: 0,
  },
  getters: {
    getEngineTemp() {
      return this.state.engineTemperature
    }
  },
  mutations: {},
  actions: {},
})

export default store;