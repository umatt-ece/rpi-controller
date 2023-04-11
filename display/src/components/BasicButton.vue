<template>
  <div class="button-container">

    <!-- Button Icon -->
    <div class="button-icon-container" v-if="icon">
      <img :src="require('../assets/images/icons/' + icon + '')" class="button-icon" alt="?"/>
    </div>

    <!-- Button Text -->
    <div class="button-text umatt-text" v-if="text">
      <h3>{{ text }}</h3>
    </div>

  </div>
</template>

<script>
export default {
  name: "BasicButton",
  props: {
    text: {
      type: String,
      default: ""
    },
    icon: {
      type: String,
      default: ""
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styling.scss";

.button-container {
  // color
  background-color: $buttonBackground;
  // border styling
  border: 3px solid $buttonBorder;
  border-radius: 5px;
  // align content horizontally & vertically to the center
  display: flex;
  justify-content: center;
  align-items: center;
}
.button-container:hover {
  // color
  background-color: $buttonHover;
}

/* icon styling */
.button-icon-container {
  // align content horizontally & vertically to the center
  display: flex;
  justify-content: center;
  align-items: center;
}
.button-icon {
  // image sizing
  max-height: 60px;
  max-width: 60px;
}

/* text styling */
.button-text {
  // margin & padding
  margin-left: 0.5em;
}
</style>