// VueJs App
import { createApp } from "vue"
import App from "./App.vue"
// router
import router from "./router"
// Vuex Store
import store from "./store"
// FontAwesome Icons
import { library } from "@fortawesome/fontawesome-svg-core"
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import { fas } from "@fortawesome/free-solid-svg-icons"


// Create a FontAwesome data-store and add all solid (fas) and regular (far) icons to it.
library.add(fas)

// Create the actual VueJs App
createApp(App)
    .use(router)
    .use(store)
    .component("fa", FontAwesomeIcon)
    .mount("#app")
