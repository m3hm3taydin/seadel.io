import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import EndpointMixin from "@/mixins/EndpointMixin.vue";
import GlobalMixin from "@/mixins/GlobalMixin.vue";
import VueGridLayout from "vue-grid-layout";
import axios from "axios";
import VueAxios from "vue-axios";
import Vuex from "vuex";
import vuetify from "./plugins/vuetify";
import Vuetify from "vuetify/lib";

Vue.config.productionTip = false;

// Plugin & Component
Vue.use(VueGridLayout);

Vue.use(VueAxios, axios);
Vue.use(Vuetify)

Vue.use(Vuex);

// Mixins
Vue.mixin(EndpointMixin);
Vue.mixin(GlobalMixin);


new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount("#app");

// Vue.config.errorHandler = function(err, vm, info) {
//   alert("[Global Error Handler]: Error in " + info + ": " + err);
// };
