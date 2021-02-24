import Vue from 'vue'
import VueRouter from 'vue-router'
import Global from "../components/GlobalData";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Login',
        component: () => import('../views/Login')
    },
    {
        path: '/homepage',
        name: 'HomePage',
        component: () => import('../views/HomePage')
    },
    {
        path: '/about',
        name: 'About',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
    },
    {
        path: '/advanced',
        name: 'Advanced',
        component: () => import('../views/Advanced')
    },
    {
        path: '/normal',
        name: 'Normal',
        component: () => import('../views/Normal')
    },
    {
        path: '/signup',
        name: 'SignUp',
        component: () => import('../views/SignUp')
    },
    {
        path: '/acctmgr',
        name: 'AcctMgr',
        component: () => import('../views/AcctMgr')
    },
]

// 2021-2-23 mjh 不登录就可以访问的页面
const freePages = [
    'Login',
    'SignUp',
    'About'
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

router.beforeEach((to, from, next) => {
    if (freePages.indexOf(to.name) < 0) {
        if (!Global.isAuthenticated) {
            next({name: 'Login'})
        } else {
            next()
        }
    } else {
        next()
    }
})

export default router
