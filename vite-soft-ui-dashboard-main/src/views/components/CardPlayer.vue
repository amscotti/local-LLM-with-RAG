<template>
  <div
    class="card card-background card-background-mask-success move-on-hover align-items-start"
  >
    <div class="cursor-pointer">
      <div
        class="full-background"
         :style="{
      backgroundImage:`url(${bgImg})`,
    }"
      ></div>
      <div class="card-body">
        <h5 class="mb-0 text-white">Some Kind Of Blues</h5>
        <p class="text-sm text-white">Deftones</p>
        <div class="mt-5 d-flex">
          <button
            class="p-2 mb-0 btn btn-outline-white rounded-circle"
            type="button"
            data-bs-toggle="tooltip"
            data-bs-placement="top"
            title="Prev"
          >
            <i class="p-2 fas fa-backward"></i>
          </button>
          <button
            class="p-2 mx-2 mb-0 btn btn-outline-white rounded-circle"
            type="button"
            data-bs-toggle="tooltip"
            data-bs-placement="top"
            title="Pause"
          >
            <i class="p-2 fas fa-play"></i>
          </button>
          <button
            class="p-2 mb-0 btn btn-outline-white rounded-circle"
            type="button"
            data-bs-toggle="tooltip"
            data-bs-placement="top"
            title="Next"
          >
            <i class="p-2 fas fa-forward"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import bgImg from '@/assets/img/curved-images/curved1.jpg'
export default {
  name: "CardPlayer",
  data() {
    return {
      bgImg
    }
  },
};
</script>
