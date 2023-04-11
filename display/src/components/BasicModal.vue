<template>
  <transition name="modal-fade">
    <div class="modal-backdrop">
      <div class="modal-container">

        <header class="modal-header" id="modalTitle">

          <!-- Modal Icon -->
          <div class="modal-icon-container" v-if="icon">
            <img :src="require('../assets/images/icons/' + icon + '')" class="modal-icon" alt="?"/>
          </div>

          <!-- Modal Title -->
          <span class="modal-title umatt-text">
            <h1>
              {{ title }}
            </h1>
          </span>

          <!-- Modal 'Close' Button -->
          <button type="button" class="modal-button-close" @click="close">
            X
          </button>

        </header>

        <section class="modal-body" id="modalDescription">

          <!-- Modal Content -->
          <div class="modal-description umatt-text">
            {{ description }}
          </div>

        </section>

        <footer class="modal-footer">

          <!-- Modal 'Accept' Button -->
          <div class="modal-button-accept-container">
            <BasicButton class="modal-button-accept" text="Accept" @click="close" />
          </div>

        </footer>

      </div>
    </div>
  </transition>
</template>

<script>
import BasicButton from "@/components/BasicButton.vue";

export default {
  name: 'BasicModal',
  components: { BasicButton },
  props: {
    icon: {
      type: String,
      default: ""
    },
    title: {
      type: String,
      default: ""
    },
    description: {
      type: String,
      default: ""
    },
  },
  methods: {
    close() {
      this.$emit('close');
    },
  },
};
</script>

<style lang="scss">
@import "@/assets/styling.scss";

/* modal backdrop (greyed out screen) */
.modal-backdrop {
  // sizing to take up the entire screen
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  // color (alpha: 0.3) for greyed effect
  background-color: rgba(0, 0, 0, 0.3);
  // position the modal in the center of the screen
  display: flex;
  justify-content: center;
  align-items: center;
}

/* modal section styling */
.modal-container {
  // sizing
  width: 50%;
  height: 32%;
  // color
  background: $modalBackground  ;
  // border styling
  border: 3px solid $modalBorder;
  border-radius: 5px;
  box-shadow: 2px 2px 20px 1px;
  // align content vertically
  display: flex;
  flex-direction: column;
  // padding and margin
  padding-top: 10px;
}
.modal-header .modal-footer {
  // padding & margin
  padding: 15px;
  display: flex;
}
.modal-header {
  // align content horizontally
  display: flex;
  flex-direction: row;
  // padding & margin
  margin: 10px;
  // idk why but this is necessary for the X button to show up...
  position: relative;
}
.modal-footer {
  // align contents vertically
  flex-direction: column;
}
.modal-body {
  // padding & margin
  position: relative;
  padding: 20px 10px;
}

/* title styling */
.modal-title {
  // align content horizontally to the center
  display: flex;
  align-items: center;
  // padding and margin
}

/* description styling */
.modal-description {
  // text styling
  font-size: 20px;
  // padding & margin
  margin: 20px;
}

/* icon styling */
.modal-icon-container {
  // align content horizontally & vertically to the center
  display: flex;
  justify-content: center;
  align-items: center;
  // padding & margin
  margin: 0 20px;
}
.modal-icon {
  // image sizing
  max-height: 60px;
  max-width: 60px;
}

/* close button styling */
.modal-button-close {
  position: absolute;
  top: 0;
  right: 0;
  border: none;
  font-size: 30px;
  padding: 15px 30px;
  cursor: pointer;
  font-weight: bold;
  color: $umattBrown;
  background: transparent;
}

/* accept button styling */

.modal-button-accept-container {
  // align content horizontally to the left
  display: flex;
  align-items: flex-start;
  // padding and margin
  margin-left: 40px;
}
.modal-button-accept{
  // size
  width: 20em;
  height: 3em;
}

/* transition styling */
.modal-fade-enter,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity .5s ease;
}

h1 {
  margin: 0;
}
</style>