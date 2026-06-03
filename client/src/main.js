import Vue from 'vue';
import VueBootstrap from 'bootstrap-vue';
import VueAxios from 'vue-axios';
import VueMoment from 'vue-moment';
// import VueSocketIO from 'vue-socket.io';
import axios from 'axios';
import numFormat from 'vue-filter-number-format';

import App from './App.vue';
import store from './store';
import routes from './routes';

Vue.filter('numFormat', numFormat);

Vue.use(VueBootstrap);
Vue.use(VueMoment);
Vue.use(VueAxios, axios);

// Vue.use(new VueSocketIO({
//     debug: false,
//     connection: process.env.VUE_APP_BASE_SOCKET,
//     vuex: {
//         store,
//         actionPrefix: 'SOCKET_',
//     },
//     options: { path: '/socket.io' }
// }));

// GitHub Pages (mode ghpages): VUE_APP_BASE_API diisi ngrok URL dari .env.ghpages
// Lokal / LAN              : selalu HTTPS karena backend berjalan dengan SSL
axios.defaults.baseURL = process.env.VUE_APP_BASE_API
    || `https://${window.location.hostname}:8000`;
axios.defaults.headers['Content-type'] = 'application/json';
// Bypass halaman interstitial ngrok agar request langsung ke backend
axios.defaults.headers['ngrok-skip-browser-warning'] = 'true';

global.Vue = Vue;

(async () => {
    const router = await routes.instance();
    return new Vue({
        router,
        store,
        render: h => h(App),
        created: function () {
            window.router = router;
        }
    }).$mount('#app');
})();

window._store = store;
