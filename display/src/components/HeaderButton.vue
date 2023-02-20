<template>
  <div class="button-container-header">
    <div class="button-styling-header">
      {{ text }}
    </div>
  </div>

</template>

<script>
export default {
  name: "HeaderButton",
  props: {
    text: String
  }
}
</script>

<style>

.button-container-header {
  display: flex;
  justify-content: center;
  align-items: center
}

.button-styling-header {
  /* background and border */
  background-color: grey;
  border: 2px solid black;
  border-radius: 5px;

  /* enforce that the button maintains a 1:1 width:height aspect ratio */
  width: 90%;
  height: 0;
  padding-bottom: 90%;

  /* text formatting */
  text-align: center;
  vertical-align: middle;
  line-height: 100%;
  font-size: 12px;
  font-family: serif;
  font-weight: bold;
}
</style>