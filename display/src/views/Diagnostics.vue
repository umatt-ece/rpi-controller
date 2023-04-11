<template>
  <div class="diagnostics-grid diagnostics-container">

    <!-- Voltage Diagnostics -->
    <div class="diagnostics-grid-item">
      <BasicInfo icon="gear.png" description="Voltage" :value="voltage" unit="V" class="diagnostics-basic-info"/>
    </div>

    <!-- GSL Position Diagnostics -->
    <div class="diagnostics-grid-item">
      <BasicInfo icon="gear.png" description="GSL Position" :value="gslPosition" unit="°" class="diagnostics-basic-info"/>
    </div>

    <!-- Diff Lock Position Diagnostics -->
    <div class="diagnostics-grid-item">
      <BasicInfo icon="gear.png" description="Diff Lock Position" :value="diffLockPosition" class="diagnostics-basic-info"/>
    </div>

    <!-- Brake Interlock Diagnostics -->
    <div class="diagnostics-grid-item">
      <BasicInfo icon="gear.png" description="Brake Interlock" :value="brakeInterlock" class="diagnostics-basic-info"/>
    </div>

    <!-- Seat Interlock Diagnostics -->
    <div class="diagnostics-grid-item">
      <BasicInfo icon="gear.png" description="Seat Interlock" :value="seatInterlock" class="diagnostics-basic-info"/>
    </div>

    <!-- Neutral Interlock Diagnostics -->
    <div class="diagnostics-grid-item">
      <BasicInfo icon="gear.png" description="Neutral Interlock" :value="neutralInterlock" class="diagnostics-basic-info"/>
    </div>

    <!-- Engine Speed Diagnostics -->
    <div class="diagnostics-grid-item">
      <BasicInfo icon="gear.png" description="Engine Speed" :value="engineSpeed" unit="RPM" class="diagnostics-basic-info"/>
    </div>

    <!-- Oil Pressure Diagnostics -->
    <div class="diagnostics-grid-item">
      <BasicInfo icon="gear.png" description="Oil Pressure" :value="oilPressure" unit="PSI" class="diagnostics-basic-info"/>
    </div>

    <!-- High Voltage System Diagnostics -->
    <div class="diagnostics-grid-item">
      <BasicInfo icon="gear.png" description="High Voltage System" :value="highVoltageSystem" class="diagnostics-basic-info"/>
    </div>

    <!-- Electric Motor Speed Diagnostics -->
    <div class="diagnostics-grid-item">
      <BasicInfo icon="gear.png" description="Electric Motor Speed" :value="electricMotorSpeed" unit="RPM" class="diagnostics-basic-info"/>
    </div>

  </div>
</template>

<script>
import BasicInfo from "@/components/BasicInfo.vue";
export default {
  name: "UmattDiagnostics",
  components: { BasicInfo },
  data() {
    return {
      genericInfo: "Unknown",
      voltage: 13.9,
      gslPosition: 0,
      diffLockPosition: "unlocked",
      brakeInterlock: "off",
      seatInterlock: "on",
      neutralInterlock: "off",
      engineSpeed: 3590,
      oilPressure: 50.0,
      highVoltageSystem: "on",
      electricMotorSpeed: 2000,
      implementInterlock: "NA",
      brakeAwayInterlock: "on",
      throttleInterlock: "off"
    }
  }
}
</script>

<style lang="scss">
@import "@/assets/styling.scss";

/* container layouts */
.diagnostics-container {
  // color
  background-color: $diagnosticsBackground;
  // border styling
  border: 3px solid $diagnosticsBorder;
  border-radius: 5px;
  // margin & padding
  margin: 10px;
  padding: 10px;
}

/* grid layout */
.diagnostics-grid {
  display: grid;
  grid-template-rows: 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr 1fr;
  gap: 5px 5px;
}
.diagnostics-grid-item {

}
</style>