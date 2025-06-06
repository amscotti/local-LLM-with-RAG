<template>
  <div class="form-check form-switch">
    <input
      :id="id"
      class="form-check-input"
      :class="inputClass"
      type="checkbox"
      :name="name"
      :checked="modelValue"
      @change="updateValue($event)"
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
    modelValue: {
      type: Boolean,
      default: false
    },
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
  methods: {
    updateValue(event) {
      this.$emit('update:modelValue', event.target.checked);
    }
  }
};
</script>
