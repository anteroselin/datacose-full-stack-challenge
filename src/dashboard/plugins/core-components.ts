import Vue from 'vue';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import VueTreeselect from '@riophae/vue-treeselect';

Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.component('vue-treeselect', VueTreeselect);
