<template>
  <div class="wrapper" :class="{ 'nav-open': $sidebar.showSidebar }">
    <div class="main-content" :data="sidebarBackground">

      <div @click="toggleSidebar">
        <fade-transition :duration="200" origin="center top" mode="out-in">
          <!-- your content here -->
          <router-view></router-view>
        </fade-transition>

      </div>
    </div>
  </div>
</template>
<script>
  import { FadeTransition } from 'vue2-transitions';

  export default {
    components: {
      FadeTransition
    },
    data() {
      return {
        sidebarBackground: 'vue' //vue|blue|orange|green|red|primary
      };
    },
    methods: {
      toggleSidebar() {
        if (this.$sidebar.showSidebar) {
          this.$sidebar.displaySidebar(true);
        }
      },
      close() {
        this.$sidebar.showSidebar === true
      }
    }
  };
</script>
<style lang="scss">
</style>
