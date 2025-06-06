<template>
  <div class="mb-4 card">
    <div class="p-3 card-body">
      <div class="d-flex" :class="directionReverse ? reverseDirection : ''">
        <div>
          <div class="text-center shadow icon icon-shape border-radius-md" :class="iconBackground">
            <i class="text-lg opacity-10" :class="iconClass" aria-hidden="true"></i>
          </div>
        </div>
        <div :class="contentClass">
          <div class="numbers">
            <p class="mb-0 text-sm text-capitalize font-weight-bold" :class="titleColor">{{ title }}</p>
            <h5 class="mb-0 font-weight-bolder" :class="valueColor">
              {{ value }}
              <span
                class="text-sm font-weight-bolder"
                :class="percentageColor"
              >{{ percentage }}</span>
            </h5>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CardComponent",
  props: {
    directionReverse: Boolean,
    title: {
      type: String,
      required: true,
    },
    titleColor: {
      type: String,
      default: ""
    },
    value: {
      type: String,
      default: ""
    },
    valueColor: {
      type: String,
      default: ""
    },
    percentage: {
      type: String,
      default: ""
    },
    iconClass: {
      type: String,
      required: true,
    },
    percentageColor: {
      type: String,
      default: "text-success",
    },
    iconBackground: {
      type: String,
      default: "bg-white",
    },
    contentClass: {
      type: String,
      default: ""
    },
  },
  data() {
    return {
      reverseDirection: "flex-row-reverse justify-content-between",
    };
  },
};
</script>
