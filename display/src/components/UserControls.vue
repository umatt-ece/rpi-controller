<template>
  <div class="controls-grid">
    <div class="controls-header">
      <div class="controls-title">
        Controls
      </div>
    </div>
    <ControlsButton text="cycle (?)" button-icon="recycle" class="controls-button" @click="OnButton1Clicked"/>
    <ControlsButton text="high beams" button-icon="lightbulb" class="controls-button" @click="OnButton2Clicked"/>
    <ControlsButton text="auto (?)" button-icon="gear" class="controls-button" @click="OnButton3Clicked"/>
    <ControlsButton text="lock (?)" button-icon="lock" class="controls-button" @click="OnButton4Clicked"/>
    <ControlsButton text="left (?)" button-icon="angle-left" class="controls-button" @click="OnButton5Clicked"/>
    <ControlsButton text="right (?)" button-icon="angle-right" class="controls-button" @click="OnButton6Clicked"/>
    <ControlsButton text="unused" button-icon="question" class="controls-button" @click="OnButton7Clicked"/>
    <ControlsButton text="unused" button-icon="question" class="controls-button" @click="OnButton8Clicked"/>
  </div>
</template>

<script>
import ControlsButton from "@/components/ControlsButton.vue"
import BaseService from "@/services/baseService"

export default {
  name: "UserControls",
  components: {ControlsButton},
  methods: {
    OnButton1Clicked() {
      BaseService.get("data/all")
          .then((value) => {
            console.log(value)
          })
          .catch((error) => {
            console.log(error)
          })
    },
    OnButton2Clicked() {
      BaseService.post("data/do", {"value": "helloooooo"})
          .then(() => {
            console.log("success!")
          })
          .catch((error) => {
            console.log(error)
          })
    },
    OnButton3Clicked() {
      console.log('button 3 clicked...')
    },
    OnButton4Clicked() {
      console.log('button 4 clicked...')
    },
    OnButton5Clicked() {
      console.log('button 5 clicked...')
    },
    OnButton6Clicked() {
      console.log('button 6 clicked...')
    },
    OnButton7Clicked() {
      console.log('unused button...')
    },
    OnButton8Clicked() {
      console.log('unused button...')
    }
  }
}
</script>

<style>

.controls-grid {
  /* grid properties */
  display: grid;
  grid-template-rows: 1fr 2fr 2fr 2fr 2fr;
  grid-template-columns: 1fr 1fr;
  gap: 5px 5px;
}

.controls-header {
  /* grid properties */
  grid-row: 1;
  grid-column: 1 / span 2;

  display: flex;
  align-items: center;
}

.controls-title {
  margin: auto 10px auto 10px;
  font-family: sans-serif;
  font-size: 30px;
  font-weight: bold;
}
</style>