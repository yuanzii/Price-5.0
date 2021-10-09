import Vue from "vue";
import App from "./App.vue";
import 'material-design-icons-iconfont/dist/material-design-icons.css';

Vue.config.productionTip = false;

import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");


import api from "./interface/index";

Vue.prototype.$api = api.commonUrl