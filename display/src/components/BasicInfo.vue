<template>
  <div class="info-grid info-container">

    <!-- Info Icon -->
    <div class="info-grid-item-one info-icon-container" v-if="icon">
      <img :src="require('../assets/images/icons/' + icon + '')" class="info-icon" alt="?"/>
    </div>

    <!-- Info Description -->
    <div class="info-grid-item-two info-description umatt-text">
      <h3>{{ description }}:</h3>
    </div>

    <!-- Info Value -->
    <div class="info-grid-item-three info-value umatt-text">
      <h3>{{ value }} {{ unit }}</h3>
    </div>

  </div>
</template>

<script>
export default {
  name: "BasicInfo",
  props: {
    icon: {
      type: String,
      default: ""
    },
    description: {
      type: String,
      default: ""
    },
    value: {
      type: String,
      default: ""
    },
    unit: {
      type: String,
      default: ""
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styling.scss";

.info-container {
  // color
  background-color: $infoBackground;
  // border styling
  border: 3px solid $infoBorder;
  border-radius: 5px;
  // align content horizontally & vertically to the center
  display: flex;
  justify-content: center;
  align-items: center;
  // size:
  height: 90%
}

/* grid layout */
.info-grid {
  display: grid;
  grid-template-columns: 1fr 6fr 6fr;
  gap: 5px 5px;
}
.info-grid-item-one {
  grid-column: 1;
}
.info-grid-item-two {
  grid-column: 2;
}
.info-grid-item-three {
  grid-column: 3;
}

/* icon styling */
.info-icon-container {
  // align content horizontally & vertically to the center
  display: flex;
  justify-content: center;
  align-items: center;
}
.info-icon {
  // image sizing
  max-height: 40px;
  max-width: 40px;
}

/* description/value styling */
.info-description {
  // text styling
  font-size: 1.5em;
}
.info-value {
  // align content horizontally to right
  display: flex;
  justify-content: end;
  // text styling
  font-size: 1.8em;
  // margin & padding
  margin-right: 1em;
}

h3 {
  // resize upper/lower margins for h3
  margin: 0.3em 0;
}
</style>