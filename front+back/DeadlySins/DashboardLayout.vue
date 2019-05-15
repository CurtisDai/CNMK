<template>
  <div class="wrapper" :class="{ 'nav-open': $sidebar.showSidebar }">
    <side-bar
      :background-color="sidebarBackground"
      short-title="Deadly Sins"
      title="Deadly sins"
    >
      <template slot="links">
        <sidebar-item
          :link="{
            name: 'Chart',
            icon: 'ni ni-tv-2 text-primary',
            path: '/dashboard'
          }"
        />

        <sidebar-item :link="{name: 'Map', icon: 'ni ni-planet text-blue', path: '/map1'}"/>
        <button @click="toggleSidebar">close</button>
      </template>
    </side-bar>
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
          this.$sidebar.displaySidebar(false);
        }
      },
      close() {
        this.$sidebar.showSidebar === false
      }
    }
  };
</script>
<style lang="scss">
</style>
