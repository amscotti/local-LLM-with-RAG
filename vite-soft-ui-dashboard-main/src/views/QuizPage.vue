<template>
  <div class="container-fluid py-4">
    <div class="row">
      <div class="col-12">
        <div class="card mb-4">
          <div class="card-header pb-0">
            <h6>Тесты и анкеты</h6>
          </div>
          <div class="card-body px-0 pt-0 pb-2">
            <QuizTable />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import QuizTable from './components/QuizTable.vue';

export default {
  name: "QuizPage",
  components: {
    QuizTable
  },
  data() {
    return {
      userId: localStorage.getItem("userId")
    };
  },
  created() {
    if (!this.userId) {
      this.$router.push("/sign-in");
    }
  }
};
</script>

<style scoped>
/* Дополнительные стили при необходимости */
</style>