<template>
  <div class="home-container">

    <!-- Primary Info --------------------------------------------->
    <div class="home-primary-grid home-primary-container">
      <!-- Speed Info -->
      <div class="home-primary-grid-item">
        <span class="umatt-text speed-info">
          {{ this.$store.state.speed }}
        </span>
        <span class="umatt-text speed-unit">
          Km/Hr
        </span>
      </div>

      <!-- Torque Info -->
      <div class="home-primary-grid-item">
        <span class="umatt-text torque-info">
          {{ this.$store.state.torque }}
        </span>
        <span class="umatt-text torque-unit">
          RPM
        </span>
      </div>

      <!-- Gear Info -->
      <div class="home-primary-grid-item">
        <span class="home-primary-info gear-info">
          {{ GearText }}
        </span>
        <img src="../assets/images/icons/tractor.png" class="gear-icon" alt="?"/>
      </div>
    </div>

    <!-- Secondary Info ------------------------------------------->
    <div class="home-secondary-grid home-secondary-container">
      <!-- Engine Temperature Info -->
      <div class="home-secondary-grid-item">
        <BasicInfo icon="temp-half.png" description="Oil Temperature" :value="this.$store.state.oilTemp" unit="°C" class="home-basic-info"/>
      </div>

      <!-- Engine Power Info -->
      <div class="home-secondary-grid-item">
        <BasicInfo icon="engine-battery.png" description="Oil Pressure" :value="this.$store.state.oilPressure" unit="PSI" class="home-basic-info"/>
      </div>

      <!-- Engine Speed Info -->
      <div class="home-secondary-grid-item">
        <BasicInfo icon="engine-belt.png" description="GSL Position" :value="this.$store.state.gslPosition" unit="°" class="home-basic-info"/>
      </div>

      <!-- Power Info -->
<!--      <div class="home-secondary-grid-item">-->
<!--        <BasicInfo icon="power-bolt.png" description="Power" :value="power" unit="V" class="home-basic-info"/>-->
<!--      </div>-->

      <!-- Drive Hours Info -->
      <div class="home-secondary-grid-item">
        <BasicInfo icon="hourglass.png" description="Drive Hours" :value="driveHours" unit="Hr" class="home-basic-info"/>
      </div>

      <!-- System Time Info -->
      <div class="home-secondary-grid-item">
        <BasicInfo icon="time.png" description="System Time" :value="systemTime" class="home-basic-info"/>
      </div>
    </div>

  </div>
</template>

<script>
import BasicInfo from "@/components/BasicInfo.vue";

export default {
  name: "UmattHome",
  components: { BasicInfo },
  data() {
    return {
      /* Primary Info */
      speed: this.$store.state.speed,
      torque: this.$store.state.torque,
      gear: this.$store.state.gear,  // 0: 'park', 1: 'reverse', 2: 'neutral', 3: 'drive'
      /* Secondary Info */
      engineTemp: this.$store.state.engineTemp,
      enginePower: this.$store.state.enginePower,
      engineSpeed: this.$store.state.engineSpeed,
      power: this.$store.state.power,
      driveHours: this.$store.state.driveHours,
      systemTime: this.$store.state.systemTime,
    }
  },
  computed: {
    GearText() {
      if (this.$store.state.gear === 0) {
        return "P"
      } else if (this.$store.state.gear === 1) {
        return "R"
      } else if (this.$store.state.gear === 2) {
        return "N"
      } else if (this.$store.state.gear === 3) {
        return "D"
      } else {
        return ""
      }
    },
  }
}
</script>

<style lang="scss">
@import "@/assets/styling.scss";

/* container layouts */
.home-container {
  // color
  background-color: $homeBackground;
  // border styling
  border: 3px solid $infoBorder;
  border-radius: 5px;
  // margin & padding
  margin: 10px;
  padding: 10px;
}
.home-primary-container {
  // color
  background-color: $homeBackground;
  // border styling
  border: 3px solid $homeBorder;
  border-radius: 5px;
  // size
  height: 38%;
  // margin & padding
  margin: 10px;
  padding: 10px;
}
.home-secondary-container {
  // color
  background-color: $homeBackground;
  // border styling
  //border: 3px solid $infoBorder;
  //border-radius: 5px;
  // margin & padding
  margin: 10px;
  padding: 10px;
}

/* grid layout */
.home-primary-grid {
  display: grid;
  grid-template-columns: 3fr 3fr 2fr;
  gap: 5px 5px;
}
.home-secondary-grid {
  display: grid;
  grid-template-rows: 1fr 1fr 1fr 1fr 1fr 1fr;
  gap: 5px 5px;
}
.home-primary-grid-item {
  // align content horizontally & vertically to the center
  display: flex;
  justify-content: center;
  align-items: center;
}
.home-secondary-grid-item {

}

/* info styling */
.speed-info {
  // text styling
  font-size: 8em;
  font-weight: bold;
}
.speed-unit {
  // text styling
  font-size: 32px;
  font-weight: bold;
  // margin & padding
  margin-left: 10px;
}
.torque-info {
  // text styling
  font-size: 6em;
  font-weight: bold;
}
.torque-unit {
  // text styling
  font-size: 32px;
  font-weight: bold;
  // margin & padding
  margin-left: 10px;
}
.gear-info {
  // text styling
  font-size: 9em;
  font-weight: bold;
}
.gear-icon {
  // image sizing
  max-height: 70px;
  max-width: 70px;
  // margin & padding
  margin-left: 15px;
}
.home-basic-info {

}
</style>