<template>
  <div class="header-container">

    <!-- UMATT Logo -->
    <div class="logo-container">
      <img src="../assets/images/umatt-logo.png" class="umatt-logo" alt="UMATT logo">
    </div>

    <!-- UMATT Text -->
    <div class="header-text">
      <h1 class="umatt-text">
        UMATT Controller 2023
      </h1>
    </div>

    <!-- Navigation Bar -->
    <div class="navbar-container umatt-text">
      <router-link to="/" class="navbar-item">
        <h1 class="umatt-text navbar-text">
          Home
        </h1>
      </router-link>
      <router-link to="/settings" class="navbar-item">
        <h1 class="umatt-text navbar-text">
          Settings
        </h1>
      </router-link>
      <router-link to="/diagnostics" class="navbar-item">
        <h1 class="umatt-text navbar-text">
          Diagnostics
        </h1>
      </router-link>
    </div>

    <!-- Toggle Fullscreen Button -->
    <div class="fullscreen-button" @click="$emit('toggleFullscreen')">
      <img :src="require('../assets/images/icons/fullscreen.png')" class="fullscreen-button" alt="Toggle Fullscreen"/>
    </div>

  </div>
</template>

<script>
export default {
  name: "AppHeader",
}
</script>

<style lang="scss">
@import "@/assets/styling.scss";

.header-container {
  // grid properties
  display: grid;
  grid-template-columns: 1fr 4fr 6fr 1fr;
  gap: 0 0;
  // color
  background-color: $headerBackground;
}

/* logo styling */
.logo-container {
  // grid properties
  grid-column: 1;
  // align content horizontally & vertically to the center
  display: flex;
  justify-content: center;
  align-items: center;
}
.umatt-logo {
  height: 4.5em;  // will maintain aspect ratio by specifying only height
}

/* header text styling */
.header-text {
  // grid properties
  grid-column: 2;
  // margin & padding
  margin: auto 10px auto 10px;
}

/* top navigation (nav) bar styling */
.navbar-container {
  // grid properties
  grid-column: 3;
  // align content horizontally to the right
  display: flex;
  justify-content: flex-end;
  // margin & padding
  padding-right: 1em;
}
.navbar-item {
  // remove router-link styling
  text-decoration: none;
  // align content horizontally & vertically to the center
  display: flex;
  justify-content: center;
  align-items: center;
  // margin & padding
  width: 20%;
  padding: 0 2em;
}
.navbar-text {
  // font styling
  font-weight: normal;  // over-ride h1 font-weight
}
/* navbar-text styling on hover */
.navbar-text:hover {
  // font styling
  font-weight: bold;  // over-ride h1 font-weight
}
/* navbar-text styling when active view (TODO: Not Working) */
.navbar-text.router-link-active {
  // font styling
  font-weight: bold; // over-ride h1 font-weight
}

/* toggle-fullscreen button */
.fullscreen-button {
  // grid properties
  grid-column: 4;
  // margin & padding
  margin: auto 10px auto 10px;
  // image sizing
  max-height: 40px;
  max-width: 40px;
}
</style>