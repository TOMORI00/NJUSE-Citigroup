import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'

import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import VueGoogleCharts from 'vue-google-charts';

Vue.config.productionTip = false

Vue.use(Antd)
Vue.use(ElementUI)
Vue.use(VueGoogleCharts)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
