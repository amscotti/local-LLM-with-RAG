<template>
  <div id="sidenavCard" class="shadow-none card card-background card-background-mask-secondary">
    <div class="full-background" :style="{ 'background-image': 'url(' + imgWhiteCurved + ')' }"></div>
    <div class="p-3 card-body text-start w-100">
      <div
        class="mb-3 text-center bg-white shadow icon icon-shape icon-sm d-flex align-items-center justify-content-center border-radius-md"
      >
        <i
          id="sidenavCardIcon"
          class="top-0 text-lg text-dark text-gradient"
          aria-hidden="true"
          :class="iconClass"
        ></i>
      </div>
      <div v-if="$store.state.isRTL" class="docs-info">
        <h6 class="mb-0 text-white up text-end">تحتاج مساعدة ؟</h6>
        <p class="text-xs font-weight-bold text-end">يرجى التحقق من مستنداتنا</p>
        <a :href="href" target="_blank" class="mb-0 btn btn-white btn-sm w-100">توثيق</a>
      </div>
      <div v-else class="docs-info">
        <h6 class="mb-0 text-white up">{{ textPrimary }}</h6>
        <p class="text-xs font-weight-bold">{{ textSecondary }}</p>
        <a :href="href" target="_blank" class="mb-0 btn btn-white btn-sm w-100">{{ linkText }}</a>
      </div>
    </div>
  </div>
</template>
<script>
import imgWhiteCurved from "../../assets/img/curved-images/white-curved.jpeg";
export default {
  name: "SidenavCard",
  props: {
    textPrimary: {
      type: String,
      default: ""
    },
    textSecondary: {
      type: String,
      default: ""
    },
    href: {
      type: String,
      default: ""
    },
    linkText: {
      type: String,
      default: ""
    },
    iconClass: {
      type: String,
      default: ""
    },
  },
  data() {
    return {
      imgWhiteCurved,
    };
  },
};
</script>
