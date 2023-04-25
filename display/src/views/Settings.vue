<template>
  <!--  <div class="settings-grid">-->
  <!--    <div class="settings-grid-item settings-nested-grid">-->
  <!--      <SettingsButton text="change units"/>-->
  <!--      <SettingsButton :text="units"/>-->
  <!--    </div>-->
  <!--    <div class="settings-grid-item settings-nested-grid">-->
  <!--      <SettingsButton text="set time"/>-->
  <!--      <SettingsButton :text="time"/>-->
  <!--    </div>-->
  <!--    <div class="settings-grid-item settings-reset">-->
  <!--      <SettingsButton text="reset" class="reset-button"/>-->
  <!--    </div>-->
  <!--    <div class="settings-grid-item">-->
  <!--      <SettingsSlider/>-->
  <!--    </div>-->
  <!--  </div>-->
  <div class="settings-container settings-grid">

    <!-- Data Logging -->
    <div class="settings-grid-item settings-toggle-item">
      <!-- Description -->
      <div class="settings-description umatt-text">
        <h3>Data Logging:</h3>
      </div>
      <!-- Value -->
      <div class="settings-value">
        <BasicToggle/>  <!-- TODO: link data() -->
      </div>
    </div>

    <!-- GenSet Mode -->
    <div class="settings-grid-item settings-toggle-item">
      <!-- Description -->
      <div class="settings-description umatt-text">
        <h3>GenSet Mode:</h3>
      </div>
      <!-- Value -->
      <div class="settings-value">
        <BasicToggle/>  <!-- TODO: link data() -->
      </div>
    </div>

    <!-- GSL Control Profile -->
    <div class="settings-grid-item settings-toggle-item">
      <!-- Description -->
      <div class="settings-description umatt-text">
        <h3>GSL Control Profile:</h3>
      </div>
      <!-- Value -->
      <div class="settings-value umatt-text">
        <h3>Linear</h3>  <!-- TODO: make into a computed property based on data() -->
      </div>
    </div>

    <!-- Units -->
    <div class="settings-grid-item settings-toggle-item">
      <!-- Description -->
      <div class="settings-description umatt-text">
        <h3>Units:</h3>
      </div>
      <!-- Value -->
      <div class="settings-value umatt-text">
        <h3>Metric</h3>  <!-- TODO: make into a computed property based on data() -->
      </div>
    </div>

    <!-- Pull Mode Activation Threshold -->
    <div class="settings-grid-item settings-slider-item">
      <!-- Description -->
      <div class="settings-description umatt-text">
        <h3>Pull Mode Activation Threshold</h3>
      </div>
      <!-- Value -->
      <div class="settings-slider umatt-text">
        <BasicSlider/>
      </div>
    </div>

    <!-- AUX I/O Options Menu -->
    <div class="settings-link-item">
      <div class="umatt-text">
        <BasicButton class="aux-button" text="AUX I/O Options Menu"/>
      </div>
    </div>

  </div>
</template>

<script>
import BasicToggle from "@/components/BasicToggle.vue";
import BasicButton from "@/components/BasicButton.vue";
import BasicSlider from "@/components/BasicSlider.vue";

export default {
  name: "UmattSettings",
  components: { BasicSlider, BasicButton, BasicToggle },
  data() {
    return {}
  }
}
</script>

<style lang="scss">
@import "@/assets/styling.scss";

/* container layouts */
.settings-container {
  // color
  background-color: $settingsBackground;
  // border styling
  border: 3px solid $settingsBorder;
  border-radius: 5px;
  // margin & padding
  margin: 10px;
  padding: 10px;
}

/* grid layout */
.settings-grid {
  display: grid;
  grid-template-rows: 1fr 1fr 1fr 1fr 4fr 1fr;
  gap: 5px 5px;
}
.settings-grid-item {
  // color
  background-color: $infoBackground;
  // border styling
  border: 3px solid $infoBorder;
  border-radius: 5px;
  // size:
  height: 90%
}

.settings-toggle-item {
  // align content vertically to the center
  display: flex;
  align-items: center;
}
.settings-link-item {
  // align content horizontally & vertically to the center
  display: flex;
  align-items: center;
  justify-content: center;
}
.settings-slider-item {
  // align content horizontally & vertically to the center
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.settings-description {
  // text styling
  font-size: 1.5em;
  // margin & padding
  margin: 0 20px;
}
.settings-value {
  // text styling
  font-size: 1.8em;
  // align right
  margin-left: auto;
  // margin & padding
  margin-right: 30px;
}
.settings-slider {
  // text styling
  font-size: 1.8em;
  font-weight: bold;
  // size
  width: 80%;
  // margin & padding
  margin: 25px;
}
.aux-button {
  // text styling
  font-size: 1.5em;
  // size
  width: 30em;
  height: 2em;
}
</style>