<template>
  <div class="header-container">
    <span class="header-logo">
      <img src="../assets/umatt-logo-bad.png" class="umatt-logo" alt="UMATT logo">
    </span>
    <span class="header-text">
      UMATT
    </span>
    <span class="header-link-container">
      <router-link to="/" class="header-link">
        Home
      </router-link>
      <router-link to="/settings" class="header-link">
        Settings
      </router-link>
      <router-link to="/diagnostics" class="header-link">
        Diagnostics
      </router-link>
    </span>
  </div>
</template>

<script>
export default {
  name: "AppHeader",
}
</script>

<style>

.header-container {
  display: flex;
  align-items: center;
}

.header-text {
  margin: auto 10px auto 10px;
  font-family: sans-serif;
  font-size: 30px;
  font-weight: bold;
}

.header-logo {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 5px;
}

.umatt-logo {
  height: 3.5em;
  width: 3.5em;
}

.header-link-container {
  display: flex;
  justify-content: flex-end;
  width: 100%;
  margin-right: 10px;
}

.header-link {
  text-align: center;
  padding: 15px 15px;
  text-decoration: none;
  color: black;
  font-family: sans-serif;
  font-size: 25px;
}

</style>