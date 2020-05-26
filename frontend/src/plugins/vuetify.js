// src/plugins/vuetify.js

import Vue from "vue";
import Vuetify, { VSnackbar, VBtn, VIcon } from "vuetify/lib";
import "vuetify/dist/vuetify.min.css";
import VuetifyToast from "vuetify-toast-snackbar";

Vue.use(Vuetify, {
  components: {
    VSnackbar,
    VBtn,
    VIcon
  }
});

Vue.use(VuetifyToast);

const opts = {};

export default new Vuetify(opts);
