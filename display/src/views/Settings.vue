<template>
  <div class="settings-grid">
    <div class="settings-grid-item settings-nested-grid">
      <SettingsButton text="change units"/>
      <SettingsButton :text="units"/>
    </div>
    <div class="settings-grid-item settings-nested-grid">
      <SettingsButton text="set time"/>
      <SettingsButton :text="time"/>
    </div>
    <div class="settings-grid-item settings-reset">
      <SettingsButton text="reset" class="reset-button"/>
    </div>
    <div class="settings-grid-item">
      <SettingsSlider/>
    </div>
  </div>
</template>

<script>
import SettingsButton from "@/components/SettingsButton.vue"
import SettingsSlider from "@/components/SettingsSlider.vue"
export default {
  name: "UMATT-Settings",
  components: { SettingsButton, SettingsSlider },
  data() {
    return {
      units: "metric",
      time: "00:00:0000",
    }
  }
}
</script>

<style>

.settings-grid {
  /* grid properties */
  display: grid;
  grid-template-rows: 1fr 1fr 1fr 2fr;
  grid-template-columns: 1fr;
  gap: 5px 5px;
}

.settings-grid-item {
  /* background and border */
  background-color: lightblue;
  border: 2px solid black;
  border-radius: 5px;
}

.settings-nested-grid {
  /* grid properties */
  display: grid;
  grid-template-rows: 1fr;
  grid-template-columns: 1fr 1fr;
}

.settings-reset {
  display: grid;
}

</style>