import axios from "axios"


const baseUrl = "http://localhost:8577/"

export default class BaseService {

  static get(url) {
    return axios.get(baseUrl + url, BaseService.getHeader()).then(res => res ? res.data : null);
  }

  static post(url, data = {}) {
    return axios.post(baseUrl + url, data, BaseService.getHeader()).then(res => res ? res.data : null);
  }

  static getHeader() {
    return {
      "headers": {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest"
      }
    }
  }
}