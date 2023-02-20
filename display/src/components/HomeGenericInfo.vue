<template>
  <div class="home-generic-grid">
    <HomeGenericButton :value="engineTemperature" unit="°C" icon="temperature-half" class="home-generic-grid-item"/>
    <HomeGenericButton value="Engine Power" unit="%" icon="battery-half" class="home-generic-grid-item"/>
    <HomeGenericButton value="Engine Speed" unit="RPM" icon="gauge-high" class="home-generic-grid-item"/>
    <HomeGenericButton value="Power" unit="V" icon="bolt" class="home-generic-grid-item"/>
    <HomeGenericButton value="Time (?)" unit="Hr" icon="hourglass" class="home-generic-grid-item"/>
    <HomeGenericButton value="Time (?)" icon="clock" class="home-generic-grid-item"/>
  </div>
</template>

<script>
import HomeGenericButton from "@/components/HomeGenericButton.vue";
export default {
  name: "GenericInfo",
  components: { HomeGenericButton },
  computed: {
    engineTemperature() {
      return this.$store.state.engineTemperature.toFixed(1)
    }
  }
}
</script>

<style>

.home-generic-grid {
  /* grid properties */
  display: grid;
  grid-template-rows: 1fr 1fr;
  grid-template-columns: 1fr 1fr 1fr;

  width: 100%;
  height: 100%;
}

.home-generic-grid-item {

}

</style>