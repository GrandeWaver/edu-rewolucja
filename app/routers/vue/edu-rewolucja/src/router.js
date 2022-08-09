import {createRouter, createWebHistory} from 'vue-router'
import Login from './vievs/Login-Screen.vue';
import WelcomeBack from './vievs/WelcomeBack-Screen.vue'
import Register from './vievs/Register-Screen.vue';
import Dashboard from './vievs/Dashboard-Screen.vue'
import cookies from './scripts/cookies';

import RegisterTutor from './vievs/footer/RegisterTutor-Screen.vue'
import Contact from './vievs/footer/Contact-Screen.vue'
import PrivacyPolicy from './vievs/footer/PrivacyPolicy-Screen.vue'
import TermsAndConditions from './vievs/footer/TermsAndConditions-Screen.vue'

import BuyLesson from './vievs/BuyLesson-Screen.vue'

import SelectSubject from './vievs/new_class/SelectSubject-Screen.vue'
import SelectTutor from './vievs/new_class/SelectTutor-Screen.vue'
import SelectRank from './vievs/new_class/SelectRank-Screen.vue'
import SelectDate from './vievs/new_class/SelectDate-Screen.vue'
import SelectSchedule from './vievs/new_class/SelectSchedule-Screen.vue'

import nProgress from 'nprogress';

  const routes = [
      {
        path: '/',
        name: 'Dashboard',
        component: Dashboard,
      },
      {
        path: '/login',
        name: 'Login',
        component: Login,
      },
      {
        path: '/welcome-back',
        name: 'WelcomeBack',
        component: WelcomeBack,
      },
      {
        path: '/register',
        name: 'Register',
        component: Register,
      },
      {
        path: '/register-tutor',
        name: 'RegisterTutor',
        component: RegisterTutor,
      },
      {
        path: '/contact',
        name: 'Contact',
        component: Contact,
      },
      {
        path: '/privacy-policy',
        name: 'PrivacyPolicy',
        component: PrivacyPolicy,
      },
      {
        path: '/terms-and-conditions',
        name: 'TermsAndConditions',
        component: TermsAndConditions,
      },
      {
        path: '/buy-lesson/:id',
        name: 'BuyLesson',
        component: BuyLesson,
        props: true
      },
      {
        path: '/new-class/subject',
        name: 'NewClass-subject',
        component: SelectSubject,
      },
      {
        path: '/new-class/tutor/:subject',
        name: 'NewClass-tutor',
        component: SelectTutor,
        props: true
      },
      {
        path: '/new-class/rank/:subject',
        name: 'NewClass-rank',
        component: SelectRank,
        props: true
      },
      {
        path: '/new-class/date/:subject',
        name: 'NewClass-date',
        component: SelectDate,
        props: true
      },
      {
        path: '/new-class/schedule/:subject',
        name: 'NewClass-schedule',
        component: SelectSchedule,
        props: true
      },
  ]
  
  const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
  })

  router.beforeEach((to, from, next) => {
    nProgress.start()
    if (to.name == 'RegisterTutor' || to.name == 'Contact' || to.name == 'PrivacyPolicy' || to.name == 'TermsAndConditions'){
      next()
      return
    } if (cookies.getCookie('auth') == undefined && to.name == 'Login' || to.name == 'Register') {
      next()
      return
    } if (cookies.getCookie('auth') != undefined && to.name == 'Login' || to.name == 'Register') {
      next('/')
    } if (cookies.getCookie('auth') == undefined && to.name == 'Dashboard') {
      next('/login')
    } else {
      next()
    }
  });

  router.afterEach(() => {
    nProgress.done()
  })

  export default router;