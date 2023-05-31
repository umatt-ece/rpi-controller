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
    store.dispatch('fetchSpeed');
    }, 3000); // Poll every 1 second

// eslint-disable-next-line no-constant-condition
while(true) {
    setInterval();
}