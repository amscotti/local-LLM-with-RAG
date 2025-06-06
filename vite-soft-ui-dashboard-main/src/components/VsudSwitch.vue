<template>
  <div class="form-check form-switch">
    <input
      :id="id"
      class="form-check-input"
      :class="inputClass"
      type="checkbox"
      :name="name"
      :checked="checked"
    />
    <label class="form-check-label" :class="labelClass" :for="id">
      <slot />
    </label>
  </div>
</template>

<script>
export default {
  name: "VsudSwitch",
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
    labelClass: {
      type: String,
      default: ""
    },
    inputClass: {
      type: String,
      default: ""
    },
  },
};
</script>
