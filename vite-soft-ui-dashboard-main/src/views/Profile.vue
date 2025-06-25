<template>
  <div class="container-fluid">
    <div
      class="mt-4 page-header min-height-300 border-radius-xl"
      :style="{
        backgroundImage:`url(${bgImg})`,

        backgroundPositionY: '50%',
      }"
    >
      <span class="mask bg-gradient-success opacity-6"></span>
    </div>
    <div class="mx-4 overflow-hidden card card-body blur shadow-blur mt-n6">
      <div class="row gx-4">
        <div class="col-auto">
          <!-- <div class="avatar avatar-xl position-relative">
            <img
              src="../assets/img/bruce-mars.jpg"
              alt="profile_image"
              class="shadow-sm w-100 border-radius-lg"
            />
          </div> -->
        </div>
        <div class="col-auto my-auto">
          <div class="h-100">
            <h5 class="mb-1">{{ user.login }} - <span class="text-sm">{{ user.full_name }}</span></h5>
            <p class="mb-0 text-sm font-weight-bold">Отдел: {{ user.department_name }}</p>
            <p class="mb-0 text-sm font-weight-bold">Доступ: {{ user.access_name }}</p>
            
          </div>
        </div>
        <div
          class="mx-auto mt-3 col-lg-4 col-md-6 my-sm-auto ms-sm-auto me-sm-0"
        >
          <div class="nav-wrapper position-relative end-0">
           
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="py-4 container-fluid">
    <div class="mt-3 row">

      <!-- <div class="mt-4 col-12 col-md-6 col-xl-4 mt-md-0">
       
      </div> -->
      
    </div>
    
  </div>
</template>

<script>
import VsudSwitch from "@/components/VsudSwitch.vue";
import ProfileCard from "./components/ProfileCard.vue";
import VsudAvatar from "../components/VsudAvatar.vue";
import sophie from "@/assets/img/kal-visuals-square.jpg";
import marie from "@/assets/img/marie.jpg";
import ivana from "@/assets/img/ivana-square.jpg";
import peterson from "@/assets/img/team-4.jpg";
import nick from "@/assets/img/team-3.jpg";
import img1 from "@/assets/img/home-decor-1.jpg";
import img2 from "@/assets/img/home-decor-2.jpg";
import img3 from "@/assets/img/home-decor-3.jpg";
import team1 from "@/assets/img/team-1.jpg";
import team2 from "@/assets/img/team-2.jpg";
import team3 from "@/assets/img/team-3.jpg";
import team4 from "@/assets/img/team-4.jpg";
import bgImg from "@/assets/img/curved-images/curved14.jpg"
import ProjectsCard from "./components/ProjectOverviewCard.vue";

import setNavPills from "@/assets/js/nav-pills.js";
import setTooltip from "@/assets/js/tooltip.js";
import axios from "axios";

export default {
  name: "ProfileOverview",
  components: {
    VsudSwitch,
    ProfileCard,
    VsudAvatar,
    ProjectsCard,
  },
  data() {
    return {
      showMenu: false,
      sophie,
      marie,
      ivana,
      peterson,
      nick,
      img1,
      team1,
      team2,
      team3,
      team4,
      img2,
      img3,
      bgImg,
      user: {
        login: "",
        role_id: "",
        department_name: "",
        access_id: ""
      }
    };
  },

  mounted() {
    this.$store.state.isAbsolute = true;
    this.$store.state.isNavFixed = false;
    setNavPills();
    setTooltip();
    this.fetchUserData();
  },
  beforeUnmount() {
    this.$store.state.isAbsolute = false;
  },
  methods: {
    async fetchUserData() {
      try {
        const userId = localStorage.getItem("userId"); // Получаем ID пользователя из localStorage
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/user/user/${userId}`);  // Замените 1 на нужный ID пользователя
        this.user = response.data;
      } catch (error) {
        console.error("Ошибка при получении данных пользователя:", error);
      }
    }
  }
};
</script>
