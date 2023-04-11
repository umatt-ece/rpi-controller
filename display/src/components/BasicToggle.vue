<template>
  <div class="toggle-container">
    <label class="toggle-switch">
      <input type="checkbox">
      <span class="toggle-slider"></span>
    </label>
  </div>
</template>

<script>
export default {
  name: 'BasicToggle',
};
</script>

<style lang="scss">
@import "@/assets/styling.scss";

.toggle-container {
  font-size: 30px;
  height: 50px;
}

/* toggle-switch (box around the toggle-slider) */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 70px;
  height: 40px;
}

/* hide default HTML checkbox */
.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* toggle-slider */
.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
  border-radius: 40px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 32px;
  width: 32px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: #2196F3;
}

input:focus + .toggle-slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .toggle-slider:before {
  //-webkit-transform: translateX(26px);
  //-ms-transform: translateX(30px);
  transform: translateX(30px);
}
</style>