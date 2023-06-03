<template>
  <div class="controls-grid controls-container">

    <!-- Button 1: Headlights -->
    <div class="controls-button-container grid-full-button">
      <BasicButton class="controls-button-full"
                   :text="HeadlightsText"
                   :icon="HeadlightsIcon"
                   @click="HeadlightsButtonClicked"/>
    </div>

    <!-- Button 2: Left Indicator -->
    <div class="controls-button-container">
      <BasicButton v-if="!leftIndicatorActive"
                   class="controls-button-half-left"
                   icon="arrow-left.png"
                   @click="LeftIndicatorButtonClicked"/>
      <BasicButton v-else
                   class="controls-button-half-left blinker-button"
                   icon="arrow-left.png"
                   @click="LeftIndicatorButtonClicked"/>
    </div>

    <!-- Button 3: Right Indicator -->
    <div class="controls-button-container">
      <BasicButton v-if="!rightIndicatorActive"
                   class="controls-button-half-right"
                   icon="arrow-right.png"
                   @click="RightIndicatorButtonClicked"/>
      <BasicButton v-else
                   class="controls-button-half-right blinker-button"
                   icon="arrow-right.png"
                   @click="RightIndicatorButtonClicked"/>
    </div>

    <!-- Button 4: Transmission State (?) -->
    <div class="controls-button-container grid-full-button">
      <BasicButton class="controls-button-full"
                   text="Transmission State"
                   icon="arrow-cycle.png"
                   @click="TestButton"/>
    </div>

    <!-- Button 5: Tow Mode -->
    <div class="controls-button-container grid-full-button">
      <BasicButton class="controls-button-full"
                   :text="TowModeText"
                   icon="gear-bold.png"
                   @click="TowModeButtonClicked"/>
    </div>

    <!-- Button 6: Differential Lock -->
    <div class="controls-button-container grid-full-button">
      <BasicButton class="controls-button-full"
                   text="Differential Lock"
                   :icon="DiffLockIcon"
                   @click="DiffLockButtonClicked"/>
    </div>

  </div>
</template>

<script>
import BaseService from "@/services/baseService"
import BasicButton from "@/components/BasicButton.vue"

export default {
  name: "AppControls",
  components: {BasicButton},
  data() {
    return {
      headlightState: 0,  // 0: 'off', 1: 'low', 2: 'high'
      leftIndicatorActive: false,
      rightIndicatorActive: false,
      towMode: 1,  // 0: 'manual', 1: 'automatic'
      diffLock: false,
    }
  },
  mounted() {
    // TODO: load initial data from API
  },
  methods: {
    HeadlightsButtonClicked() {
      console.log("headlights toggled")
      // cycle values between 0 -> 1 -> 2 -> 0 ...
      this.headlightState = (this.headlightState + 1) % 3

      // test
      BaseService.post("sys/test")
          .then(() => {
            console.log("success!")
          })
          .catch((error) => {
            console.log(error)
          })

    },
    LeftIndicatorButtonClicked() {
      console.log("left indicator toggled")
      this.leftIndicatorActive = !this.leftIndicatorActive
    },
    RightIndicatorButtonClicked() {
      console.log("right indicator toggled")
      this.rightIndicatorActive = !this.rightIndicatorActive
    },
    UnknownButtonClicked() {
      console.log("unknown button function...")
    },
    TowModeButtonClicked() {
      fetch('http://localhost:8577/sys/toggle-tow-mode', {
        method: 'POST',
      })
        .then(response => {
          if (response.ok) {
            // Success, handle the response
            console.log('Tow mode toggled successfully');
            // Perform any additional actions if needed
          } else {
            // Error, handle the response
            console.error('Error toggling tow mode');
          }
        })
        .catch(error => {
          // Network or other error occurred
          console.error('Request failed:', error);
        });

      // cycle values between 0 -> 1 -> 0 ...
      this.towMode = (this.towMode + 1) % 2
    },
    DiffLockButtonClicked() {
      fetch('http://localhost:8577/sys/toggle-diff-lock', {
        method: 'POST',
      })
        .then(response => {
          if (response.ok) {
            // Success, handle the response
            console.log('Differential lock toggled successfully');
            // Perform any additional actions if needed
          } else {
            // Error, handle the response
            console.error('Error toggling differential lock');
          }
        })
        .catch(error => {
          // Network or other error occurred
          console.error('Request failed:', error);
        });
      this.diffLock = !this.diffLock
    },
    TestButton() {
      BaseService.get("sys/get", {"value": "helloooooo"})
          .then(() => {
            console.log("success!")
          })
          .catch((error) => {
            console.log(error)
          })
    }
  },
  computed: {
    HeadlightsIcon() {
      if (this.headlightState === 0) {
        return ""
      } else if (this.headlightState === 1) {
        return "low-beams.png"
      } else if (this.headlightState === 2) {
        return "high-beams.png"
      } else {
        return ""
      }
    },
    HeadlightsText() {
      if (this.headlightState === 0) {
        return "Headlights OFF"
      } else if (this.headlightState === 1) {
        return "Low Beams"
      } else if (this.headlightState === 2) {
        return "High Beams"
      } else {
        return ""
      }
    },
    TowModeText() {
      if (this.towMode === 0) {
        return "Tow: MANUAL"
      } else if (this.towMode === 1) {
        return "Tow: AUTO"
      } else {
        return ""
      }
    },
    DiffLockIcon() {
      return this.diffLock ? "lock-close.png" : "lock-open.png"
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styling.scss";

.controls-container {
  background-color: $controlsBackground;
}

/* grid layout */
.controls-grid {
  display: grid;
  grid-template-rows: 1fr 1fr 1fr 1fr 1fr;
  grid-template-columns: 1fr 1fr;
}
.grid-full-button {
  grid-column: 1 / span 2;
}

/* button styling */
.controls-button-container {
  // align content horizontally & vertically to the center
  display: flex;
  justify-content: center;
  align-items: center;
  // text styling
  font-size: 20px;
}
.controls-button-full {
  // width & height
  width: 90%;
  height: 75%;
}
.controls-button-half-left {
  // width & height
  width: 85%;
  height: 75%;
  // margin & padding
  margin-left: 0.5em;
}
.controls-button-half-right {
  // width & height
  width: 80%;
  height: 75%;
  // margin & padding
  margin-right: 0.5em;
}

/* blinker-button animation */
.blinker-button {
  animation: blink-animation 1s steps(5, start) infinite;
  -webkit-animation: blink-animation 1s steps(5, start) infinite;
}
@keyframes blink-animation {
  to {
    visibility: hidden;
  }
}
@-webkit-keyframes blink-animation {
  to {
    visibility: hidden;
  }
}
</style>