<template>
  <div class="form-group">
    <label :for="exampleFormControlTextarea1">
      <slot />
    </label>
    <textarea
      :id="exampleFormControlTextarea1"
      class="form-control"
      rows="5"
      :placeholder="placeholder"
    ></textarea>
  </div>
</template>

<script>
export default {
  name: "VsudTextarea",
  props: {
    id: {
      type: String,
      default: ""
    },
    placeholder: {
      type: String,
      default: ""
    },
  },
};
</script>