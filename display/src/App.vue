<template>
  <div class="app-grid app-container">
    <AppHeader class="app-grid-item app-grid-header"/>
    <AppControls class="app-grid-item app-grid-controls"/>
    <router-view class="app-grid-item app-grid-view"/>
    <BasicModal v-show="serviceReminder" icon="caution.png" title="Service Reminder" :description="serviceReminderText"/>
  </div>
</template>

<script>
import AppHeader from "@/components/AppHeader.vue"
import AppControls from "@/components/AppControls.vue"
import BasicModal from "@/components/BasicModal.vue"
import {useStore} from "vuex";
export default {
  name: "App",
  components: { AppHeader, AppControls, BasicModal },
  data() {
    return {
      serviceReminder: false,
      serviceTimeNext: 4,
      serviceTimeLast: 96,
    }
  },
  setup() {
    const store = useStore()
    store.dispatch("liveData/update")
  },
  computed: {
    serviceReminderText() {
      return `The next oil change is due in ${this.serviceTimeNext} hours.\n` +
          ` The time since the last oil change has been ${this.serviceTimeLast} hours.` +
          ` For more details regarding service operations, please refer to the operator's manual.`
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styling.scss";

/* ensure app is full size of window */
body {
  margin: 0;
  padding: 0;
}

.app-container {
  background-color: $umattWhite;
  height: 100vh;
  width: 100vw;
}

/* grid layout */
.app-grid {
  display: grid;
  grid-template-rows: 1fr 8fr;
  grid-template-columns: 1fr 3fr;
  gap: 0 0;
}
.app-grid-item {}
.app-grid-header {
  grid-row: 1;
  grid-column: 1 / span 2;
}
.app-grid-controls {
  grid-row: 2;
  grid-column: 1;
}
.app-grid-view {
  grid-row: 2;
  grid-column: 2;
}
</style>