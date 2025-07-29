import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const routes = [
  { name:"app.input", path: "/input", component: require('./views/itembarang.vue').default },
  { name:"app.search", path: "/search", component: require('./views/SearchItem.vue').default },
  { name:"app", path: "/", redirect: "/input" },  // Redirect ke input sebagai default
];

export default {
    instance: async () => {
        const resp = new Router({
            base: process.env.BASE_URL,
            linkActiveClass: 'open active',
            scrollBehavior: () => ({ y: 0 }),
            routes
        })
        return resp;
    }
};
