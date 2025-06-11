<template>
  <div class="card card-blog card-plain">
    <div class="position-relative">
      <a class="shadow-xl d-block border-radius-xl">
        <img :src="img" alt="img-blur-shadow" class="shadow img-fluid border-radius-xl" />
      </a>
    </div>
    <div class="px-1 pb-0 card-body">
      <p class="mb-2 text-sm text-gradient text-dark">Project #{{ number }}</p>
      <a href="javascript:;">
        <h5>{{ title }}</h5>
      </a>
      <p class="mb-4 text-sm">{{ description }}</p>
      <div class="d-flex align-items-center justify-content-between">
        <button type="button" class="mb-0 btn btn-outline-success btn-sm">View Project</button>
        <div class="mt-2 avatar-group">
          <a
            href="javascript:;"
            class="avatar avatar-xs rounded-circle"
            data-bs-toggle="tooltip"
            data-bs-placement="bottom"
            :title="titleTeam1"
          >
            <img alt="Image placeholder" :src="imgTeam1" />
          </a>
          <a
            href="javascript:;"
            class="avatar avatar-xs rounded-circle"
            data-bs-toggle="tooltip"
            data-bs-placement="bottom"
            :title="titleTeam2"
          >
            <img alt="Image placeholder" :src="imgTeam2" />
          </a>
          <a
            href="javascript:;"
            class="avatar avatar-xs rounded-circle"
            data-bs-toggle="tooltip"
            data-bs-placement="bottom"
            :title="titleTeam3"
          >
            <img alt="Image placeholder" :src="imgTeam3" />
          </a>
          <a
            href="javascript:;"
            class="avatar avatar-xs rounded-circle"
            data-bs-toggle="tooltip"
            data-bs-placement="bottom"
            :title="titleTeam4"
          >
            <img alt="Image placeholder" :src="imgTeam4" />
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProjectsCard",
  props: {
    img: {
      type: String,
      default: ""
    },
    number: {
      type: Number,
      default: 0
    },
    title: {
      type: String,
      default: ""
    },
    description: {
      type: String,
      default: ""
    },
    imgTeam1: {
      type: String,
      default: ""
    },
    imgTeam2: {
      type: String,
      default: ""
    },
    imgTeam3: {
      type: String,
      default: ""
    },
    imgTeam4: {
      type: String,
      default: ""
    },
    titleTeam1: {
      type: String,
      default: ""
    },
    titleTeam2: {
      type: String,
      default: ""
    },
    titleTeam3: {
      type: String,
      default: ""
    },
    titleTeam4: {
      type: String,
      default: ""
    },
  },
};
</script>
