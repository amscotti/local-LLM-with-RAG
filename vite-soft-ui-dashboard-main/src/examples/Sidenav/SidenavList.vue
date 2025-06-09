<template>
  <div
    id="sidenav-collapse-main"
    class="w-auto h-auto collapse navbar-collapse max-height-vh-100 h-100"
  >
    <ul class="navbar-nav">
      <li class="nav-item">
        <sidenav-collapse nav-text="Главная" :to="{ name: 'Dashboard' }">
          <template #icon>
            <icon name="dashboard" />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse nav-text="Админская панель" :to="{ name: 'Tables' }">
          <template #icon>
            <icon name="tables" />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse nav-text="Счета" :to="{ name: 'Billing' }">
          <template #icon>
            <icon name="billing" />
          </template>
        </sidenav-collapse>
      </li>

      <li class="nav-item">
        <sidenav-collapse nav-text="Виртуальная реальность" :to="{ name: 'Virtual Reality' }">
          <template #icon>
            <icon name="virtual-reality" />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse nav-text="Правый интерфейс" :to="{ name: 'Rtl' }">
          <template #icon>
            <icon name="rtl-page" />
          </template>
        </sidenav-collapse>
      </li>
      <li class="mt-3 nav-item">
        <h6
          class="text-xs ps-4 text-uppercase font-weight-bolder opacity-6"
          :class="$store.state.isRTL ? 'me-4' : 'ms-2'"
        >СТРАНИЦЫ</h6>
      </li>
      <li class="nav-item">
        <sidenav-collapse nav-text="Профиль" :to="{ name: 'Profile' }">
          <template #icon>
            <icon name="customer-support" />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse nav-text="Вход" :to="{ name: 'Sign In' }">
          <template #icon>
            <icon name="sign-in" />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <sidenav-collapse nav-text="Регистрация" :to="{ name: 'Sign Up' }">
          <template #icon>
            <icon name="sign-up" />
          </template>
        </sidenav-collapse>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#" @click.prevent="handleLogout">
          <div
            class="icon icon-shape icon-sm shadow border-radius-md bg-white text-center d-flex align-items-center justify-content-center me-2"
          >
            <i class="ni ni-button-power text-danger"></i>
          </div>
          <span class="nav-link-text ms-1">Выход</span>
        </a>
      </li>
    </ul>
  </div>
  <div class="pt-3 mx-3 mt-3 sidenav-footer">
    <sidenav-card
      :class="cardBg"
      text-primary="Нужна помощь?"
      text-secondary="Проверьте нашу документацию"
      href="https://www.creative-tim.com/learning-lab/vue/overview/soft-ui-dashboard/"
      link-text="Документация"
      icon-class="ni ni-diamond"
    />
    <a
      class="btn bg-gradient-success mt-4 w-100"
      href="https://www.creative-tim.com/product/vue-soft-ui-dashboard-pro?ref=vsud"
      type="button"
    >Версия Про</a>
  </div>
</template>
<script>
import Icon from "@/components/Icon.vue";
import SidenavCollapse from "./SidenavCollapse.vue";
import SidenavCard from "./SidenavCard.vue";
import { mapActions } from "vuex";
import { useRouter } from "vue-router";

export default {
  name: "SidenavList",
  components: {
    Icon,
    SidenavCollapse,
    SidenavCard,
  },
  props: {
    cardBg: {
      type: String,
      default: ""
    },
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  data() {
    return {
      title: "Vite Soft UI Dashboard",
      controls: "dashboardsExamples",
      isActive: "active",
    };
  },
  methods: {
    ...mapActions(['logout']),
    handleLogout() {
      this.logout();
      this.router.push('/sign-in');
    },
    getRoute() {
      const routeArr = this.$route.path.split("/");
      return routeArr[1];
    },
  },
};
</script>
