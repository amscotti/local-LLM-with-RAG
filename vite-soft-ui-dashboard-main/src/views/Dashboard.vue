<template>
  <div class="py-4 container-fluid">
    <div class="row">
      <div v-for="card in cards" :key="card.id" class="col-xl-3 col-sm-6 mb-xl-0 mb-4">
        <card
          :title="card.title"
          :value="card.description"
          :percentage="card.file_path"
          :icon-class="stats.iconClass"
          :icon-background="stats.iconBackground"
          direction-reverse
          :userId="Number(userId)"
        ></card>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-7 mb-lg-0 mb-4">
        <div class="card">
          <div class="card-body p-3">
            <div class="row">
              <div class="col-lg-6">
                <div class="d-flex flex-column h-100">
                  <p class="mb-1 pt-2 text-bold">Built by developers</p>
                  <h5 class="font-weight-bolder">Vite Soft UI Dashboard</h5>
                  <p class="mb-5">
                    From colors, cards, typography to complex elements, you will
                    find the full documentation.
                  </p>
                  <a
                    class="text-body text-sm font-weight-bold mb-0 icon-move-right mt-auto"
                    href="javascript:;"
                  >
                    Read More
                    <i
                      class="fas fa-arrow-right text-sm ms-1"
                      aria-hidden="true"
                    ></i>
                  </a>
                </div>
              </div>
              <div class="col-lg-5 ms-auto text-center mt-5 mt-lg-0">
                <div class="bg-gradient-success border-radius-lg h-100">
                  <img
                    src="../assets/img/shapes/waves-white.svg"
                    class="position-absolute h-100 w-50 top-0 d-lg-block d-none"
                    alt="waves"
                  />
                  <div
                    class="position-relative d-flex align-items-center justify-content-center h-100"
                  >
                    <img
                      class="w-100 position-relative z-index-2 pt-4"
                      src="../assets/img/illustrations/rocket-white.png"
                      alt="rocket"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-lg-5">
        <div class="card h-100 p-3">
          <div
            class="overflow-hidden position-relative border-radius-lg bg-cover h-100"
            style="
              background-image: url('https://demos.creative-tim.com/soft-ui-dashboard/assets/img/ivancik.jpg');
            "
          >
            <span class="mask bg-gradient-dark"></span>
            <div
              class="card-body position-relative z-index-1 d-flex flex-column h-100 p-3"
            >
              <h5 class="text-white font-weight-bolder mb-4 pt-2">
                Work with the rockets
              </h5>
              <p class="text-white">
                Wealth creation is an evolutionarily recent positive-sum game.
                It is all about who take the opportunity first.
              </p>
              <a
                class="text-white text-sm font-weight-bold mb-0 icon-move-right mt-auto"
                href="javascript:;"
              >
                Read More
                <i
                  class="fas fa-arrow-right text-sm ms-1"
                  aria-hidden="true"
                ></i>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="mt-4 row">
      <div class="mb-4 col-lg-5 mb-lg-0">
        <div class="card z-index-2">
          <div class="p-3 card-body">
            <!-- chart -->
            <active-users-chart />
          </div>
        </div>
      </div>
      <div class="col-lg-7">
        <!-- line chart -->
        <div class="card z-index-2">
          <gradient-line-chart />
        </div>
      </div>
    </div>
    <div class="row my-4">
      <div class="col-lg-8 col-md-6 mb-md-0 mb-4">
        <projects-card />
      </div>
      <div class="col-lg-4 col-md-6">
        <Orders-card />
      </div>
    </div>
  </div>
</template>

<script>
import Card from "@/examples/Cards/Card.vue";
import ActiveUsersChart from "@/examples/Charts/ActiveUsersChart.vue";
import GradientLineChart from "@/examples/Charts/GradientLineChart.vue";
import OrdersCard from "./components/OrdersCard.vue";
import ProjectsCard from "./components/ProjectsCard.vue";
import axios from "axios";

export default {
  name: "DashboardDefault",
  components: {
    Card,
    ActiveUsersChart,
    GradientLineChart,
    ProjectsCard,
    OrdersCard,
  },
  data() {
    return {
      cards: [], // Массив для хранения карточек
      stats: {
        iconBackground: "bg-gradient-success",
        iconClass: "ni ni-money-coins"
      },
      userId: localStorage.getItem("userId"), // Получаем ID пользователя из localStorage
    };
  },
  async created() {
    if (!this.userId) {
      // Если ID пользователя не найден, перенаправляем на страницу входа
      this.$router.push("/sign-in");
      return;
    }
    console.log("User ID:", this.userId);
    await this.fetchCards(Number(this.userId)); // Загрузка карточек для текущего пользователя
  },
  methods: {
    async fetchCards(userId) {
      try {
        const response = await axios.get(`http://localhost:8000/user/${userId}/content`); // Новый эндпоинт
        if (Array.isArray(response.data)) {
          this.cards = response.data; // Сохранение данных в массив
          console.log('Cards:', this.cards);
        } else {
          // Если сервер вернул один объект, обернем его в массив
          this.cards = [response.data];
          console.log('Single card converted to array:', this.cards);
        }
      } catch (error) {
        console.error("Ошибка при получении карточек:", error);
      }
    },
  },
};
</script>
