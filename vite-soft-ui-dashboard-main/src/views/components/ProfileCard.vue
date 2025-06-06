<template>
  <div class="card h-100">
    <div class="p-3 pb-0 card-header">
      <div class="row">
        <div class="col-md-8 d-flex align-items-center">
          <h6 class="mb-0">Информация о пользователе</h6>
        </div>
      </div>
    </div>
    <div class="p-3 card-body">
      <hr class="my-1 horizontal gray-light" />
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
          <strong class="text-sm text-dark">Связь:</strong> &nbsp;
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
