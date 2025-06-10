<template>
  <div class="card">
    <div class="card-header pb-0">
      <div class="row">
        <div class="col-lg-6 col-7">
          <h6>Список пользователей</h6>
          <p class="text-sm mb-0">
            <i class="fa fa-check text-info" aria-hidden="true"></i>
            <span class="font-weight-bold ms-1">Всего пользователей: {{ users.length }}</span>
          </p>
        </div>
      </div>
    </div>
    <div class="card-body px-0 pt-0 pb-2">
      <div class="table-responsive p-0">
        <table class="table align-items-center mb-0">
          <thead>
            <tr>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">
                Пользователь
              </th>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">
                Роль
              </th>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">
                Отдел
              </th>
              <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">
                Уровень доступа
              </th>
              <th class="text-secondary opacity-7"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>
                <div class="d-flex px-2 py-1">
                  <div class="d-flex flex-column justify-content-center">
                    <h6 class="mb-0 text-sm">{{ user.login }}</h6>
                  </div>
                </div>
              </td>
              <td>
                <p class="text-xs font-weight-bold mb-0">{{ user.role_name }}</p>
              </td>
              <td>
                <p class="text-xs font-weight-bold mb-0">{{ user.department_name }}</p>
              </td>
              <td>
                <p class="text-xs font-weight-bold mb-0">{{ user.access_name }}</p>
              </td>
              <td class="align-middle">
                <button @click="openEditModal(user)" class="btn btn-link text-secondary mb-0">
                  <i class="fa fa-edit text-xs"></i>
                </button>
                <button @click="openPasswordModal(user)" class="btn btn-link text-secondary mb-0">
                  <i class="fa fa-key text-xs"></i>
                </button>
                <button @click="confirmDeleteUser(user)" class="btn btn-link text-danger mb-0">
                  <i class="fa fa-trash text-xs"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Модальное окно для редактирования пользователя -->
  <div class="modal fade" id="editUserModal" tabindex="-1" role="dialog" aria-labelledby="editUserModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="editUserModalLabel">Редактирование пользователя</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="userLogin">Логин</label>
            <input type="text" class="form-control" id="userLogin" v-model="editingUser.login" disabled>
          </div>
          <div class="form-group mt-3">
            <label for="departmentSelect">Отдел</label>
            <select class="form-control" id="departmentSelect" v-model="editingUser.department_id">
              <option v-for="department in departments" :key="department.id" :value="department.id">
                {{ department.name }}
              </option>
            </select>
          </div>
          <div class="form-group mt-3">
            <label for="accessLevelSelect">Уровень доступа</label>
            <select class="form-control" id="accessLevelSelect" v-model="editingUser.access_id">
              <option v-for="access in accessLevels" :key="access.id" :value="access.id">
                {{ access.name }}
              </option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
          <button type="button" class="btn btn-primary" @click="updateUser">Сохранить</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Модальное окно для смены пароля -->
  <div class="modal fade" id="passwordModal" tabindex="-1" role="dialog" aria-labelledby="passwordModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="passwordModalLabel">Сменить пароль</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="newPassword">Новый пароль</label>
            <input type="password" class="form-control" id="newPassword" v-model="newPassword">
          </div>
          <div class="form-group mt-3">
            <label for="confirmPassword">Подтвердите пароль</label>
            <input type="password" class="form-control" id="confirmPassword" v-model="confirmPassword">
          </div>
          <div v-if="passwordError" class="alert alert-danger mt-3">
            {{ passwordError }}
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
          <button type="button" class="btn btn-primary" @click="updatePassword">Сохранить</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Модальное окно для подтверждения удаления -->
  <div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="deleteModalLabel">Подтверждение удаления</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          Вы действительно хотите удалить пользователя <strong>{{ deletingUser.login }}</strong>?
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
          <button type="button" class="btn btn-danger" @click="deleteUser">Удалить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VsudAvatar from "@/components/VsudAvatar.vue";
import VsudBadge from "@/components/VsudBadge.vue";
import axios from 'axios';
import { Modal } from 'bootstrap';

export default {
  name: "AuthorsTable",
  components: {
    VsudAvatar,
    VsudBadge,
  },
  data() {
    return {
      users: [],
      departments: [],
      accessLevels: [],
      editingUser: {
        id: null,
        login: '',
        department_id: null,
        access_id: null
      },
      deletingUser: {
        id: null,
        login: ''
      },
      newPassword: '',
      confirmPassword: '',
      passwordError: '',
      editModal: null,
      passwordModal: null,
      deleteModal: null
    };
  },
  async created() {
    await this.fetchUsers();
    await this.fetchDepartments();
    await this.fetchAccessLevels();
  },
  mounted() {
    this.editModal = new Modal(document.getElementById('editUserModal'));
    this.passwordModal = new Modal(document.getElementById('passwordModal'));
    this.deleteModal = new Modal(document.getElementById('deleteModal'));
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get('http://localhost:8000/users');
        this.users = response.data;
      } catch (error) {
        console.error('Ошибка при получении пользователей:', error);
      }
    },
    async fetchDepartments() {
      try {
        const response = await axios.get('http://localhost:8000/departments');
        this.departments = response.data;
      } catch (error) {
        console.error('Ошибка при получении отделов:', error);
      }
    },
    async fetchAccessLevels() {
      try {
        const response = await axios.get('http://localhost:8000/access-levels');
        this.accessLevels = response.data;
      } catch (error) {
        console.error('Ошибка при получении уровней доступа:', error);
      }
    },
    openEditModal(user) {
      this.editingUser = {
        id: user.id,
        login: user.login,
        department_id: user.department_id,
        access_id: user.access_id
      };
      this.editModal.show();
    },
    openPasswordModal(user) {
      this.editingUser = {
        id: user.id,
        login: user.login
      };
      this.newPassword = '';
      this.confirmPassword = '';
      this.passwordError = '';
      this.passwordModal.show();
    },
    confirmDeleteUser(user) {
      this.deletingUser = {
        id: user.id,
        login: user.login
      };
      this.deleteModal.show();
    },
    async updateUser() {
      try {
        await axios.put(`http://localhost:8000/user/${this.editingUser.id}`, {
          department_id: this.editingUser.department_id,
          access_id: this.editingUser.access_id
        });
        
        this.editModal.hide();
        await this.fetchUsers();
      } catch (error) {
        console.error('Ошибка при обновлении пользователя:', error);
      }
    },
    async updatePassword() {
      this.passwordError = '';
      
      if (!this.newPassword) {
        this.passwordError = 'Пароль не может быть пустым';
        return;
      }
      
      if (this.newPassword !== this.confirmPassword) {
        this.passwordError = 'Пароли не совпадают';
        return;
      }
      
      try {
        await axios.put(`http://localhost:8000/user/${this.editingUser.id}/password`, {
          password: this.newPassword
        });
        
        this.passwordModal.hide();
      } catch (error) {
        console.error('Ошибка при обновлении пароля:', error);
        this.passwordError = error.response?.data?.detail || 'Произошла ошибка при обновлении пароля';
      }
    },
    async deleteUser() {
      try {
        await axios.delete(`http://localhost:8000/user/${this.deletingUser.id}`);
        this.deleteModal.hide();
        await this.fetchUsers();
      } catch (error) {
        console.error('Ошибка при удалении пользователя:', error);
      }
    }
  },
};
</script>