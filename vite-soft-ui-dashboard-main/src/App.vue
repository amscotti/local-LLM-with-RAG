<template>
  <sidenav
    v-if="$store.state.showSidenav"
    :custom_class="$store.state.mcolor"
    :class="[
      $store.state.isTransparent,
      $store.state.isRTL ? 'fixed-end' : 'fixed-start',
    ]"
  />
  <main
    class="main-content position-relative max-height-vh-100 h-100 border-radius-lg"
    :style="$store.state.isRTL ? 'overflow-x: hidden' : ''"
  >
    <!-- nav -->
    <navbar
      v-if="$store.state.showNavbar"
      :class="[navClasses]"
      :text-white="$store.state.isAbsolute ? 'text-white opacity-8' : ''"
      :min-nav="navbarMinimize"
    />
    <router-view />
    <app-footer v-show="$store.state.showFooter" />
    <configurator
      :toggle="toggleConfigurator"
      :class="[
        $store.state.showConfig ? 'show' : '',
        $store.state.hideConfigButton ? 'd-none' : '',
      ]"
    />
  </main>
</template>
<script>
import Sidenav from "./examples/Sidenav/index.vue";
import Configurator from "@/examples/Configurator.vue";
import Navbar from "@/examples/Navbars/Navbar.vue";
import AppFooter from "@/examples/Footer.vue";
import { mapMutations } from "vuex";
export default {
  name: "App",
  components: {
    Sidenav,
    Configurator,
    Navbar,
    AppFooter,
  },

  computed: {
    navClasses() {
      return {
        "position-sticky blur shadow-blur mt-4 left-auto top-1 z-index-sticky":
          this.$store.state.isNavFixed,
        "position-absolute px-4 mx-0 w-100 z-index-2":
          this.$store.state.isAbsolute,
        "px-0 mx-4 mt-4": !this.$store.state.isAbsolute,
      };
    },
  },
  beforeMount() {
    this.$store.state.isTransparent = "bg-transparent";
  },
  methods: {
    ...mapMutations(["toggleConfigurator", "navbarMinimize"]),
  },
};
</script>
