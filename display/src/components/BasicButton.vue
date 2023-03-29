<template>
  <div class="button-container">

    <!-- button image -->
    <div class="button-icon" v-if="icon">
      <img :src="require('../assets/images/icons/' + icon + '')" class="icon" alt="?"/>
    </div>

    <!-- button text -->
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
  border: 2px solid $buttonBorder;
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
.button-icon {
  // align content horizontally & vertically to the center
  display: flex;
  justify-content: center;
  align-items: center;
}
.icon {
  // image sizing
  max-height: 60px;
  max-width: 60px;
}

/* text styling */
.button-text {
  // margin & padding
  margin: auto 2em;
}
</style>