import { createStore } from "vuex"

import liveData from "@/store/liveData"
import storedData from "@/store/storedData"

const store = createStore({
  modules: {
    liveData, storedData
  },
  state: {
    title: "Vuex Store",
      /* ------ Home ------ */
      /* Primary Info */
      speed: liveData.state.data1,
      torque: 1849,
      gear: 1,  // 0: 'park', 1: 'drive', 2: 'reverse'
      /* Secondary Info */
      engineTemp: 182,
      enginePower: 32,
      engineSpeed: 194,
      power: 13.6,
      driveHours: 7.8,
      systemTime: "09:36",
      /* ------ Diagnostics ------ */
      genericInfo: "Unknown",
      voltage: 13.9,
      gslPosition: 0,
      diffLockPosition: "unlocked",
      brakeInterlock: "off",
      seatInterlock: "on",
      neutralInterlock: "off",
      //engineSpeed: 3590,
      oilPressure: 50.0,
      highVoltageSystem: "on",
      electricMotorSpeed: 2000,
      implementInterlock: "NA",
      brakeAwayInterlock: "on",
      throttleInterlock: "off"
  },
  getters: {
    getEngineTemp() {
      return this.state.engineTemp
    }
  },
  mutations: {
    updateSpeed(state, speed) {
      state.speed = speed;
    }
  },
  actions: {
    fetchSpeed({ commit }) {
      fetch('/sys/get_speed')
          .then(response => response.json())
          .then(data => {
            commit('updateSpeed', data);
          })
          .catch(error => {
            console.error('Error fetching speed:', error);
          });
    },
  },
})

export default store;