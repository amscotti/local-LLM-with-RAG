<template>
  <div class="container top-0 position-sticky z-index-sticky">
    <div class="row">
      <div class="col-12">
        <navbar
          is-blur="blur blur-rounded my-3 py-2 start-0 end-0 mx-4 shadow"
          btn-background="bg-gradient-success"
          :dark-mode="true"
        />
      </div>
    </div>
  </div>
  <main class="mt-0 main-content main-content-bg">
    <section>
      <div class="page-header min-vh-75">
        <div class="container">
          <div class="row">
            <div class="mx-auto col-xl-4 col-lg-5 col-md-6 d-flex flex-column">
              <div class="mt-8 card card-plain">
                <div class="pb-0 card-header text-start">
                  <h3 class="font-weight-bolder text-info text-gradient">Добро пожаловать</h3>
                  <p class="mb-0">Введите логин и пароль для входа</p>
                </div>
                <div class="card-body">
                  <form role="form" class="text-start" @submit.prevent="handleLogin">
                    <label>Логин</label>
                    <vsud-input v-model="login" type="text" placeholder="Логин" name="login" />
                    <label>Пароль</label>
                    <vsud-input v-model="password" type="password" placeholder="Пароль" name="password" />
                    <vsud-switch id="rememberMe" checked>Запомнить меня</vsud-switch>
                    <div class="text-center">
                      <vsud-button
                        class="my-4 mb-2"
                        variant="gradient"
                        color="info"
                        full-width
                        type="submit"
                      >Войти</vsud-button>
                    </div>
                    <p v-if="errorMessage" class="text-danger text-center">{{ errorMessage }}</p>
                  </form>
                </div>
                <div class="text-center pt-0 px-lg-2 px-1">
                  <p class="mb-4 text-sm mx-auto">
                    Нет аккаунта?
                    <router-link to="/sign-up" class="text-info text-gradient font-weight-bold">Зарегистрироваться</router-link>
                  </p>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="top-0 oblique position-absolute h-100 d-md-block d-none me-n8">
                <div
                  class="bg-cover oblique-image position-absolute fixed-top ms-auto h-100 z-index-0 ms-n6"
                  :style="{
                    backgroundImage:
                      `url(${bgImg})`,
                  }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
  <app-footer />
</template>

<script>
import Navbar from "@/examples/PageLayout/Navbar.vue";
import AppFooter from "@/examples/PageLayout/Footer.vue";
import VsudInput from "@/components/VsudInput.vue";
import VsudSwitch from "@/components/VsudSwitch.vue";
import VsudButton from "@/components/VsudButton.vue";
import axios from "axios";
import { useRouter } from "vue-router";
import bgImg from "@/assets/img/curved-images/curved9.jpg"
const body = document.getElementsByTagName("body")[0];

export default {
  name: "SignIn",
  components: {
    Navbar,
    AppFooter,
    VsudInput,
    VsudSwitch,
    VsudButton,
  },
  data() {
    return {
      login: "",
      password: "",
      errorMessage: "",
      bgImg
    };
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  methods: {
    async handleLogin() {
      if (!this.login || !this.password) {
        this.errorMessage = "Пожалуйста, заполните все поля";
        return;
      }
      try {
        this.errorMessage = "";
        console.log("Логин перед отправкой:", this.login);
        console.log("Пароль перед отправкой:", this.password);
        const response = await axios.post("http://localhost:8000/login", {
          login: this.login,
          password: this.password
        }, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        
        console.log("Успешная авторизация:", response.data);
        
        // Сохраняем информацию о входе пользователя
        localStorage.setItem("isAuthenticated", "true");
        localStorage.setItem("userLogin", this.login);
        
        // Перенаправляем на панель управления
        this.router.push("/dashboard");
      } catch (error) {
        console.error("Ошибка авторизации:", error);
        this.errorMessage = error.response?.data?.detail || "Произошла ошибка при авторизации";
      }
    }
  },
  created() {
    this.$store.state.hideConfigButton = true;
    this.$store.state.showNavbar = false;
    this.$store.state.showSidenav = false;
    this.$store.state.showFooter = false;
    body.classList.remove("bg-gray-100");
  },
  beforeUnmount() {
    this.$store.state.hideConfigButton = false;
    this.$store.state.showNavbar = true;
    this.$store.state.showSidenav = true;
    this.$store.state.showFooter = true;
    body.classList.add("bg-gray-100");
  },
};
</script>
