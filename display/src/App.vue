<template>
  <div class="grid-container">
    <AppHeader class="grid-item grid-header"/>
    <UserControls class="grid-item grid-controls"/>
    <router-view class="grid-item grid-info"/>
  </div>
</template>

<script>
import AppHeader from "@/components/AppHeader.vue"
import UserControls from "@/components/UserControls.vue"
import {useStore} from "vuex";
export default {
  name: "App",
  components: { AppHeader, UserControls },
  setup() {
    const store = useStore()
    store.dispatch("liveData/update")
  }
}
</script>

<style>

body {
  margin: 0;
  padding: 0;
}


.grid-container {
  /* grid properties */
  display: grid;
  grid-template-rows: 1fr 8fr;
  grid-template-columns: 1fr 3fr;
  gap: 0 0;

  background-color: aliceblue;
  height: 100vh;
  width: 100vw;
}

.grid-item {
  background-color: beige;
  border: 2px solid black;
  border-radius: 5px;
  margin: 5px;
  padding: 5px;
}

.grid-header {
  grid-row: 1;
  grid-column: 1 / span 2;
}

.grid-controls {
  grid-row: 2;
  grid-column: 1;
}

.grid-info {
  grid-row: 2;
  grid-column-start: 2;
}

</style>