<template>
  <div class="button-container-home-generic">
    <div class="button-styling-home-generic">
      <fa :icon="icon" class="button-icon-home-generic" />
      <span class="button-text-home-generic">
        {{ value }} {{ unit }}
      </span>
    </div>
  </div>

</template>

<script>
export default {
  name: "HomeGenericButton",
  props: {
    value: {
      type: String,
      default: "Unknown"
    },
    unit: {
      type: String,
      default: ""
    },
    icon: {
      type: String,
      default: "gear"
    },
  }
}
</script>

<style>

.button-container-home-generic {
  display: flex;
  justify-content: center;
  align-items: center
}

.button-styling-home-generic {
  /* background and border */
  background-color: orange;
  border: 2px solid black;
  border-radius: 5px;

  /* enforce that the button maintains a 1:1 width:height aspect ratio */
  width: 98%;
  height: 92%;

  /* contents alignment formatting */
  display: flex;
  flex-direction: row;
  justify-content: left;
  align-items: center;
}

.button-icon-home-generic {
  height: 2em;
  width: 2em;
  margin: 10px;
}

.button-text-home-generic {
  text-align: center;
  font-family: sans-serif;
  font-size: 16px;
  font-weight: bold;
}
</style>