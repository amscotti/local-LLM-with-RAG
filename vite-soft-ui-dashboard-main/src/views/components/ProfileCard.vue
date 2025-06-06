<template>
  <div class="card h-100">
    <div class="p-3 pb-0 card-header">
      <div class="row">
        <div class="col-md-8 d-flex align-items-center">
          <h6 class="mb-0">Profile Information</h6>
        </div>
        <div class="col-md-4 text-end">
          <a href="javascript:;">
            <i
              class="text-sm fas fa-user-edit text-secondary"
              data-bs-toggle="tooltip"
              data-bs-placement="top"
              title="Edit Profile"
            ></i>
          </a>
        </div>
      </div>
    </div>
    <div class="p-3 card-body">
      <p class="text-sm">
        Hi, I’m Alec Thompson, Decisions: If you can’t decide, the answer is no.
        If two equally difficult paths, choose the one more painful in the short
        term (pain avoidance is creating an illusion of equality).
      </p>
      <hr class="my-4 horizontal gray-light" />
      <ul class="list-group">
        <li class="pt-0 text-sm border-0 list-group-item ps-0">
          <strong class="text-dark">Full Name:</strong> &nbsp; Alec M. Thompson
        </li>
        <li class="text-sm border-0 list-group-item ps-0">
          <strong class="text-dark">Mobile:</strong> &nbsp; (44) 123 1234 123
        </li>
        <li class="text-sm border-0 list-group-item ps-0">
          <strong class="text-dark">Email:</strong> &nbsp; alecthompson@mail.com
        </li>
        <li class="text-sm border-0 list-group-item ps-0">
          <strong class="text-dark">Location:</strong> &nbsp; USA
        </li>
        <li class="pb-0 border-0 list-group-item ps-0">
          <strong class="text-sm text-dark">Social:</strong> &nbsp;
          <a
            class="py-0 mb-0 btn btn-facebook btn-simple ps-1 pe-2"
            href="javascript:;"
          >
            <i class="fab fa-facebook fa-lg"></i>
          </a>
          <a
            class="py-0 mb-0 btn btn-twitter btn-simple ps-1 pe-2"
            href="javascript:;"
          >
            <i class="fab fa-twitter fa-lg"></i>
          </a>
          <a
            class="py-0 mb-0 btn btn-instagram btn-simple ps-1 pe-2"
            href="javascript:;"
          >
            <i class="fab fa-instagram fa-lg"></i>
          </a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfileCard",
};
</script>
