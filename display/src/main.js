import { createApp } from "vue"
import App from "./App.vue"

import router from "./router"  // Vue Router
import store from "./store"    // Vuex Store

import "@/assets/styling.scss"  // Global SCSS assets

// Create the VueJs App
createApp(App)
    .use(router)
    .use(store)
    .mount("#app")

setInterval(() => {
    store.dispatch('fetchAll');
    }, 300); // Poll every 1 second

setInterval();