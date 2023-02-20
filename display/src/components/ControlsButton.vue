<template>
  <div class="button-container-controls">
    <div class="button-styling-controls">
      <fa :icon="buttonIcon" class="button-icon-controls" />
      <div class="button-text-controls">
        {{ text }}
      </div>
    </div>
  </div>

</template>

<script>
export default {
  name: "ControlsButton",
  props: {
    text: String,
    buttonIcon: {
      type: String,
      default: "gear"
    },
  }
}
</script>

<style>

.button-container-controls {
  display: flex;
  justify-content: center;
  align-items: center
}

.button-styling-controls {
  /* background and border */
  background-color: grey;
  border: 2px solid black;
  border-radius: 5px;

  /* enforce that the button maintains a 1:1 width:height aspect ratio */
  width: 90%;
  height: 90%;

  /* contents alignment formatting */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.button-icon-controls {
  height: 3em;
  width: 3em;
}

.button-text-controls {
  margin-top: 1em;
  text-align: center;
  font-family: sans-serif;
  font-size: 12px;
  font-weight: bold;
}
</style>