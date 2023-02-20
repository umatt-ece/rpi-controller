<template>
  <div class="home-important-grid">
    <!-- speed display -->
    <div class="home-important-grid-item">
      <div class="info-styling-home-important">
        <span class="info-text-home-speed">
          {{ currentSpeed }} Km/Hr
        </span>
      </div>
    </div>
    <!-- torque display -->
    <div class="home-important-grid-item">
      <div class="info-styling-home-important">
        <span class="info-text-home-torque">
          {{ currentTorque }} RPM
        </span>
      </div>
    </div>
    <!-- gear display -->
    <div class="home-important-grid-item">
      <div class="info-styling-home-important">
        <fa icon="car" class="info-icon-home-gear" />
        <span class="info-text-home-gear">
          {{ currentGear }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "ImportantInfo",
  computed: {
    currentSpeed() {
      return "000"
    },
    currentTorque() {
      return "000"
    },
    currentGear() {
      return "P"
    },
  }
}
</script>

<style>

.home-important-grid {
  /* grid properties */
  display: grid;
  grid-template-rows: 2fr 1fr 3fr;
  grid-template-columns: 1fr;

  width: 100%;
  height: 100%;
}

.home-important-grid-item {
  display: flex;
  justify-content: center;
  align-items: center
}

.info-styling-home-important {
  /* background and border */
  background-color: orange;
  border: 2px solid black;
  border-radius: 5px;

  /* enforce that the button maintains a 1:1 width:height aspect ratio */
  width: 99%;
  height: 94%;

  /* contents alignment formatting */
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.info-text-home-speed {
  text-align: center;
  font-family: sans-serif;
  font-size: 48px;
  font-weight: bold;
}

.info-text-home-torque {
  text-align: center;
  font-family: sans-serif;
  font-size: 32px;
  font-weight: bold;
}

.info-icon-home-gear {
  height: 6em;
  width: 6em;
  margin-right: 40px;
}

.info-text-home-gear {
  text-align: center;
  font-family: sans-serif;
  font-size: 86px;
  font-weight: bold;
}

</style>
