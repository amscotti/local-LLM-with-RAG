import { createRouter, createWebHashHistory } from "vue-router";
import Dashboard from "@/views/Dashboard.vue";
import Tables from "@/views/Tables.vue";
import Billing from "@/views/Billing.vue";
import VirtualReality from "@/views/VirtualReality.vue";
import Profile from "@/views/Profile.vue";
import Rtl from "@/views/Rtl.vue";
import SignIn from "@/views/SignIn.vue";
import SignUp from "@/views/SignUp.vue";
import QuizPage from "@/views/QuizPage.vue";
import store from "@/store";

const routes = [
  {
    path: "/",
    name: "/",
    redirect: "/dashboard",
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: "/tables",
    name: "Tables",
    component: Tables,
    meta: { requiresAuth: true }
  },
  {
    path: "/billing",
    name: "Billing",
    component: Billing,
    meta: { requiresAuth: true }
  },
  {
    path: "/virtual-reality",
    name: "Virtual Reality",
    component: VirtualReality,
    meta: { requiresAuth: true }
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: "/rtl-page",
    name: "Rtl",
    component: Rtl,
    meta: { requiresAuth: true }
  },
  {
    path: "/sign-in",
    name: "Sign In",
    component: SignIn,
    meta: { guest: true }
  },
  {
    path: "/sign-up",
    name: "Sign Up",
    component: SignUp,
    meta: { guest: true }
  },
  {
    path: "/quizzes",
    name: "Quizzes",
    component: QuizPage,
    meta: { requiresAuth: true }
  },
];

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
  linkActiveClass: "active",
});

// Защита маршрутов
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isGuest = to.matched.some(record => record.meta.guest);
  const isAuthenticated = localStorage.getItem("isAuthenticated") === "true";
  const userRole = parseInt(localStorage.getItem('role_id'));

  if (requiresAuth && !isAuthenticated) {
    next('/sign-in');
  } else if (to.path === '/tables' && userRole !== 1) {
    // Только пользователи с role_id = 1 (админы) имеют доступ к админской панели
    next('/dashboard');
  } else if (isGuest && isAuthenticated) {
    next('/dashboard');
  } else {
    next();
  }
});

export default router;
