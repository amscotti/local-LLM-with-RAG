<template>
  <div class="form-check">
    <input 
      :id="id" 
      class="form-check-input" 
      type="checkbox" 
      :name="name" 
      :checked="modelValue" 
      @change="updateValue($event)"
    />
    <label :for="id" class="custom-control-label">
      <slot />
    </label>
  </div>
</template>

<script>
export default {
  name: "VsudCheckbox",
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
  },
  methods: {
    updateValue(event) {
      this.$emit('update:modelValue', event.target.checked);
    }
  }
};
</script>
