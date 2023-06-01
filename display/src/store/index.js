import { createStore } from "vuex"

import liveData from "@/store/liveData"
import storedData from "@/store/storedData"
// import BaseService from "@/services/baseService";

const store = createStore({
  modules: {
    liveData, storedData
  },
  state: {
    title: "Vuex Store",
      /* ------ Home ------ */
      /* Primary Info */
      speed: 0,
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
    updateAll(state, data) {
      this.state.speed = data.speed;
      this.state.torque = data.rpm;
    }
  },
  actions: {
    fetchAll({ commit }) {
      fetch('http://localhost:8577/sys/data')
          .then(response => response.json())
          .then(data => {
            commit('updateAll', data);
          })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    },
  },
})

export default store;