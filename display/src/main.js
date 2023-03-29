import { createApp } from "vue"
import App from "./App.vue"

import router from "./router"  // Vue Router
import store from "./store"    // Vuex Store

import "@/assets/styling.scss"  // Global SCSS assets

// FontAwesome Icons
import { library } from "@fortawesome/fontawesome-svg-core"
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import { fas } from "@fortawesome/free-solid-svg-icons"


// Create a FontAwesome data-store and add all solid (fas) and regular (far) icons to it.
library.add(fas)

// Create the VueJs App
createApp(App)
    .use(router)
    .use(store)
    .component("fa", FontAwesomeIcon)
    .mount("#app")
