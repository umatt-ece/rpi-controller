<template>
  <div class="button-container-settings">
    <div class="button-styling-settings">
      <span class="button-text-settings">
        {{ text }}
      </span>
    </div>
  </div>

</template>

<script>
export default {
  name: "SettingsButton",
  props: {
    text: {
      type: String,
      default: ""
    }
  }
}
</script>

<style>

.button-container-settings {
  display: flex;
  justify-content: center;
  align-items: center;

  width: 100%;
  height: 100%;
}

.button-styling-settings {
  /* background and border */
  background-color: orange;
  border: 2px solid black;
  border-radius: 5px;

  /* size formatting */
  width: 98%;
  height: 92%;

  /* contents alignment formatting */
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.button-text-settings {
  text-align: center;
  font-family: sans-serif;
  font-size: 32px;
  font-weight: bold;
}

</style>