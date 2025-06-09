<template>
  <div class="py-4 container-fluid">
    <div class="row flex-column">
      <div v-for="card in cards" :key="card.id" class="col-12 mb-4">
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
