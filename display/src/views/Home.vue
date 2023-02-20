<template>
  <div class="home-grid">
    <div class="home-grid-item">
      <GenericInfo/>
    </div>
    <div class="home-grid-item">
      <ImportantInfo/>
    </div>
  </div>
</template>

<script>
import GenericInfo from "@/components/HomeGenericInfo.vue";
import ImportantInfo from "@/components/HomeImportantInfo.vue";
export default {
  name: "UMATT-Home",
  components: { GenericInfo, ImportantInfo}
}
</script>

<style>

.home-grid {
  /* grid properties */
  display: grid;
  grid-template-rows: 1fr 3fr;
  grid-template-columns: auto;
  gap: 5px 5px;
}

.home-grid-item {
  /* background and border */
  background-color: lightblue;
  border: 2px solid black;
  border-radius: 5px;
}

</style>