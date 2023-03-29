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

    <!-- Button 4: ? -->
    <div class="controls-button-container grid-full-button">
      <BasicButton class="controls-button-full"
                   text="button 4"
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


    <!--     Cycle Button -->
    <!--        <div class="button-container-controls" @click="OnButton1Clicked">-->
    <!--          <div class="button-styling-controls">-->
    <!--            <fa icon="recycle" class="button-icon-controls" />-->
    <!--            <p class="button-text-controls">-->
    <!--              Cycle-->
    <!--            </p>-->
    <!--          </div>-->
    <!--        </div>-->


    <!--
    <ControlsButton text="cycle (?)" button-icon="recycle" class="controls-button" @click="OnButton1Clicked"/>
    <ControlsButton text="high beams" button-icon="lightbulb" class="controls-button" @click="OnButton2Clicked"/>
    <ControlsButton text="auto (?)" button-icon="gear" class="controls-button" @click="OnButton3Clicked"/>
    <ControlsButton text="lock (?)" button-icon="lock" class="controls-button" @click="OnButton4Clicked"/>
    <ControlsButton text="left (?)" button-icon="angle-left" class="controls-button" @click="OnButton5Clicked"/>
    <ControlsButton text="right (?)" button-icon="angle-right" class="controls-button" @click="OnButton6Clicked"/>
    <ControlsButton text="unused" button-icon="question" class="controls-button" @click="OnButton7Clicked"/>
    <ControlsButton text="unused" button-icon="question" class="controls-button" @click="OnButton8Clicked"/>
    -->
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
      towMode: 0,  // 0: 'manual', 1: 'automatic'
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
      console.log("tow mode toggles")
      // cycle values between 0 -> 1 -> 0 ...
      this.towMode = (this.towMode + 1) % 2
    },
    DiffLockButtonClicked() {
      console.log('button 5 clicked...')
      this.diffLock = !this.diffLock
    },
    TestButton() {
      BaseService.post("data/do", {"value": "helloooooo"})
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