<template>
  <div class="settings-slider-container">
    <div class="settings-slider-container-styling">
      <div class="slider-header">
        <span class="slider-header-text">
          Pull Mode Activation Threshold
        </span>
      </div>
      <div class="slider-container">
        <span class="slider-percentage">
          {{ data }}%
        </span>
        <input type="range" min="1" max="100" :value="data" class="settings-slider">
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SettingsSlider",
  data() {
    return {
      data: 50
    }
  }
}
</script>

<style>

.settings-slider-container {
  display: flex;
  justify-content: center;
  align-items: center;

  width: 100%;
  height: 100%;
}

.settings-slider-container-styling {
  /* background and border */
  background-color: orange;
  border: 2px solid black;
  border-radius: 5px;

  /* size formatting */
  width: 98%;
  height: 92%;

  /* contents alignment formatting */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.slider-header {
  /* contents alignment formatting */
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.slider-header-text {
  text-align: center;
  font-family: sans-serif;
  font-size: 28px;
  font-weight: bold;
}

.slider-container {
  /* contents alignment formatting */
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;

  margin-top: 15px;
}

.slider-percentage {
  text-align: center;
  font-family: sans-serif;
  font-size: 16px;
  font-weight: bold;
}

.settings-slider {
  /* override default styling */
  -webkit-appearance: none;
  appearance: none;
  outline: none;

  width: 35em;
  height: 15px;
  margin-left: 2em;

  background: beige;
  border-radius: 40px;
}

/* slider handle for Chrome, Opera, Safari, Edge */
.settings-slider::-webkit-slider-thumb {
  /* override default styling */
  -webkit-appearance: none;
  appearance: none;

  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: grey;
}

/* slider handle for Firefox */
.settings-slider::-moz-range-thumb {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: grey;
}

</style>