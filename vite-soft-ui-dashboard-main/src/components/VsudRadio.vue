<template>
  <div class="form-check">
    <input :id="id" class="form-check-input" type="radio" :name="name" :checked="checked" />
    <label class="custom-control-label" :for="id">
      <slot />
    </label>
  </div>
</template>

<script>
export default {
  name: "VsudRadio",
  props: {
    name: {
      type: String,
      default: ""
    },
    id: {
      type: String,
      default: ""
    },
    checked: {
      type: String,
      default: ""
    },
  },
};
</script>
