import { createStore } from "vuex";

export default createStore({
  state: {
    hideConfigButton: false,
    isPinned: true,
    showConfig: false,
    isTransparent: "",
    isRTL: false,
    mcolor: "",
    isNavFixed: false,
    isAbsolute: false,
    showNavs: true,
    showSidenav: true,
    showNavbar: true,
    showFooter: true,
    showMain: true,
    navbarFixed:
      "position-sticky blur shadow-blur left-auto top-1 z-index-sticky px-0 mx-4",
    absolute: "position-absolute px-4 mx-0 w-100 z-index-2",
    bootstrap: {
      gray: {
        100: "#f8f9fa",
        200: "#e9ecef",
        300: "#dee2e6",
        400: "#ced4da",
        500: "#adb5bd",
        600: "#6c757d",
        700: "#495057",
        800: "#343a40",
        900: "#212529",
      },
      cyan: {
        100: "#d1eff8",
        200: "#a3dff1",
        300: "#75cfe9",
        400: "#47bfe2",
        500: "#19afdb",
        600: "#148cb0",
        700: "#0f6984",
        800: "#0a4558",
        900: "#05222c",
      },
    },
    // Данные для аутентификации
    isAuthenticated: false,
    user: null
  },
  getters: {
    isAuthenticated(state) {
      return state.isAuthenticated;
    },
    currentUser(state) {
      return state.user;
    }
  },
  mutations: {
    toggleConfigurator(state) {
      state.showConfig = !state.showConfig;
    },
    navbarMinimize(state) {
      const sidenav_show = document.querySelector(".g-sidenav-show");
      if (sidenav_show.classList.contains("g-sidenav-hidden")) {
        sidenav_show.classList.remove("g-sidenav-hidden");
        sidenav_show.classList.add("g-sidenav-pinned");
        state.isPinned = true;
      } else {
        sidenav_show.classList.add("g-sidenav-hidden");
        sidenav_show.classList.remove("g-sidenav-pinned");
        state.isPinned = false;
      }
    },
    sidebarType(state, payload) {
      state.isTransparent = payload;
    },
    cardBackground(state, payload) {
      state.mcolor = payload;
    },
    navbarFixed(state) {
      if (state.isNavFixed === false) {
        state.isNavFixed = true;
      } else {
        state.isNavFixed = false;
      }
    },
    toggleSidebarColor(state, payload) {
      state.mcolor = payload;
    },
    // Мутации для аутентификации
    LOGIN(state, userData) {
      state.isAuthenticated = true;
      state.user = userData;
      localStorage.setItem("isAuthenticated", "true");
      localStorage.setItem("userData", JSON.stringify(userData));
    },
    LOGOUT(state) {
      state.isAuthenticated = false;
      state.user = null;
      localStorage.removeItem("isAuthenticated");
      localStorage.removeItem("userData");
      localStorage.removeItem("userLogin");
    },
    RESTORE_AUTH(state) {
      const isAuthenticated = localStorage.getItem("isAuthenticated") === "true";
      const userData = JSON.parse(localStorage.getItem("userData") || "null");
      
      if (isAuthenticated && userData) {
        state.isAuthenticated = true;
        state.user = userData;
      }
    }
  },
  actions: {
    toggleSidebarColor({ commit }, payload) {
      commit("toggleSidebarColor", payload);
    },
    // Действия для аутентификации
    login({ commit }, userData) {
      commit("LOGIN", userData);
    },
    logout({ commit }) {
      commit("LOGOUT");
    },
    restoreAuthentication({ commit }) {
      commit("RESTORE_AUTH");
    }
  }
});
