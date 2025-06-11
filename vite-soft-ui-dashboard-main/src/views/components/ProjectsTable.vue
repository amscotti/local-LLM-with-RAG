<template>
  <div class="card mb-4">
    <div class="card-header pb-0">
      <h6>Projects table</h6>
    </div>
    <div class="card-body px-0 pt-0 pb-2">
      <div class="table-responsive p-0">
        <table class="table align-items-center justify-content-center mb-0">
          <thead>
            <tr>
              <th
                class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
              >
                Project
              </th>
              <th
                class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2"
              >
                Budget
              </th>
              <th
                class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2"
              >
                Status
              </th>
              <th
                class="text-uppercase text-secondary text-xxs font-weight-bolder text-center opacity-7 ps-2"
              >
                Completion
              </th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <div class="d-flex px-2">
                  <div>
                    <img
                      src="../../assets/img/small-logos/logo-invision.svg"
                      class="avatar avatar-sm rounded-circle me-2"
                      alt="spotify"
                    />
                  </div>
                  <div class="my-auto">
                    <h6 class="mb-0 text-sm">Spotify</h6>
                  </div>
                </div>
              </td>
              <td>
                <p class="text-sm font-weight-bold mb-0">$2,500</p>
              </td>
              <td>
                <span class="text-xs font-weight-bold">working</span>
              </td>
              <td class="align-middle text-center">
                <div class="d-flex align-items-center justify-content-center">
                  <span class="me-2 text-xs font-weight-bold">60%</span>
                  <div>
                    <vsud-progress
                      color="info"
                      variant="gradient"
                      percentage="60"
                    />
                  </div>
                </div>
              </td>
              <td class="align-middle">
                <button class="btn btn-link text-secondary mb-0">
                  <i class="fa fa-ellipsis-v text-xs" aria-hidden="true"></i>
                </button>
              </td>
            </tr>
            <tr>
              <td>
                <div class="d-flex px-2">
                  <div>
                    <img
                      src="../../assets/img/small-logos/logo-invision.svg"
                      class="avatar avatar-sm rounded-circle me-2"
                      alt="invision"
                    />
                  </div>
                  <div class="my-auto">
                    <h6 class="mb-0 text-sm">Invision</h6>
                  </div>
                </div>
              </td>
              <td>
                <p class="text-sm font-weight-bold mb-0">$5,000</p>
              </td>
              <td>
                <span class="text-xs font-weight-bold">done</span>
              </td>
              <td class="align-middle text-center">
                <div class="d-flex align-items-center justify-content-center">
                  <span class="me-2 text-xs font-weight-bold">100%</span>
                  <div>
                    <vsud-progress
                      color="success"
                      variant="gradient"
                      percentage="100"
                    />
                  </div>
                </div>
              </td>
              <td class="align-middle">
                <button
                  class="btn btn-link text-secondary mb-0"
                  aria-haspopup="true"
                  aria-expanded="false"
                >
                  <i class="fa fa-ellipsis-v text-xs" aria-hidden="true"></i>
                </button>
              </td>
            </tr>
            <tr>
              <td>
                <div class="d-flex px-2">
                  <div>
                    <img
                      src="../../assets/img/small-logos/logo-jira.svg"
                      class="avatar avatar-sm rounded-circle me-2"
                      alt="jira"
                    />
                  </div>
                  <div class="my-auto">
                    <h6 class="mb-0 text-sm">Jira</h6>
                  </div>
                </div>
              </td>
              <td>
                <p class="text-sm font-weight-bold mb-0">$3,400</p>
              </td>
              <td>
                <span class="text-xs font-weight-bold">canceled</span>
              </td>
              <td class="align-middle text-center">
                <div class="d-flex align-items-center justify-content-center">
                  <span class="me-2 text-xs font-weight-bold">30%</span>
                  <div>
                    <vsud-progress
                      color="danger"
                      variant="gradient"
                      percentage="30"
                    />
                  </div>
                </div>
              </td>
              <td class="align-middle">
                <button
                  class="btn btn-link text-secondary mb-0"
                  aria-haspopup="true"
                  aria-expanded="false"
                >
                  <i class="fa fa-ellipsis-v text-xs" aria-hidden="true"></i>
                </button>
              </td>
            </tr>
            <tr>
              <td>
                <div class="d-flex px-2">
                  <div>
                    <img
                      src="../../assets/img/small-logos/logo-slack.svg"
                      class="avatar avatar-sm rounded-circle me-2"
                      alt="slack"
                    />
                  </div>
                  <div class="my-auto">
                    <h6 class="mb-0 text-sm">Slack</h6>
                  </div>
                </div>
              </td>
              <td>
                <p class="text-sm font-weight-bold mb-0">$1,000</p>
              </td>
              <td>
                <span class="text-xs font-weight-bold">canceled</span>
              </td>
              <td class="align-middle text-center">
                <div class="d-flex align-items-center justify-content-center">
                  <span class="me-2 text-xs font-weight-bold">0%</span>
                  <div>
                    <vsud-progress
                      color="success"
                      variant="gradient"
                      percentage="0"
                    />
                  </div>
                </div>
              </td>
              <td class="align-middle">
                <button
                  class="btn btn-link text-secondary mb-0"
                  aria-haspopup="true"
                  aria-expanded="false"
                >
                  <i class="fa fa-ellipsis-v text-xs" aria-hidden="true"></i>
                </button>
              </td>
            </tr>
            <tr>
              <td>
                <div class="d-flex px-2">
                  <div>
                    <img
                      src="../../assets/img/small-logos/logo-invision.svg"
                      class="avatar avatar-sm rounded-circle me-2"
                      alt="webdev"
                    />
                  </div>
                  <div class="my-auto">
                    <h6 class="mb-0 text-sm">Webdev</h6>
                  </div>
                </div>
              </td>
              <td>
                <p class="text-sm font-weight-bold mb-0">$14,000</p>
              </td>
              <td>
                <span class="text-xs font-weight-bold">working</span>
              </td>
              <td class="align-middle text-center">
                <div class="d-flex align-items-center justify-content-center">
                  <span class="me-2 text-xs font-weight-bold">80%</span>
                  <div>
                    <vsud-progress
                      color="info"
                      variant="gradient"
                      percentage="80"
                    />
                  </div>
                </div>
              </td>
              <td class="align-middle">
                <button
                  class="btn btn-link text-secondary mb-0"
                  aria-haspopup="true"
                  aria-expanded="false"
                >
                  <i class="fa fa-ellipsis-v text-xs" aria-hidden="true"></i>
                </button>
              </td>
            </tr>
            <tr>
              <td>
                <div class="d-flex px-2">
                  <div>
                    <img
                      src="../../assets/img/small-logos/logo-xd.svg"
                      class="avatar avatar-sm rounded-circle me-2"
                      alt="xd"
                    />
                  </div>
                  <div class="my-auto">
                    <h6 class="mb-0 text-sm">Adobe XD</h6>
                  </div>
                </div>
              </td>
              <td>
                <p class="text-sm font-weight-bold mb-0">$2,300</p>
              </td>
              <td>
                <span class="text-xs font-weight-bold">done</span>
              </td>
              <td class="align-middle text-center">
                <div class="d-flex align-items-center justify-content-center">
                  <span class="me-2 text-xs font-weight-bold">100%</span>
                  <div>
                    <vsud-progress
                      color="success"
                      variant="gradient"
                      percentage="100"
                    />
                  </div>
                </div>
              </td>
              <td class="align-middle">
                <button
                  class="btn btn-link text-secondary mb-0"
                  aria-haspopup="true"
                  aria-expanded="false"
                >
                  <i class="fa fa-ellipsis-v text-xs" aria-hidden="true"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import VsudProgress from "@/components/VsudProgress.vue";

export default {
  name: "ProjectsTable",
  components: {
    VsudProgress,
  },
};
</script>
