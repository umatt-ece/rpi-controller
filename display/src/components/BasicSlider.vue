<template>
  <div class="slider-container">

    <!-- TODO: make 'min', 'max', and 'value' props... -->
    <div class="slider-inner-container">
      <input type="range" :min="minValue" :max="maxValue" v-bind:value="currValue" class="slider">
    </div>

    <!-- Percentage -->
    <span class="slider-percentage umatt-text">
      {{ currValue }}%
    </span>

  </div>
</template>

<script>
export default {
  name: "BasicSlider",
  data() {
    return {
      minValue: 0,
      maxValue: 100,
      currValue: 50,
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styling.scss";

.slider-container {
  // align content horizontally to the center
  display: flex;
  flex-direction: row;
  justify-content: center;
}
.slider-inner-container {
  // size
  width: 100%;
}

.slider {
  // override defaults
  -webkit-appearance: none;
  // size
  width: 100%;
  height: 18px;
  // border styling
  border-radius: 8px;
  background: #d3d3d3;
  outline: none;
  opacity: 0.7;
  // transition styling
  -webkit-transition: .2s;
  transition: opacity .2s;
}

/* Hover effect */
.slider:hover {
  opacity: 1;  // fully shown on hover
}

.slider-percentage {
  // margin & padding
  margin-left: 10px;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: #04AA6D;
  cursor: pointer;
}
.slider::-moz-range-thumb {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: #04AA6D;
  cursor: pointer;
}
</style>