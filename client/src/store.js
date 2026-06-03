import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        stream:  null,
        cart:    { display: 0, items: [], cartOwner: '' },
        loading: { active: false, message: '' },
    },
    mutations: {
        setStream(state, stream) {
            state.stream = stream;
        },
        clearStream(state) {
            if (state.stream) {
                state.stream.getTracks().forEach(track => track.stop());
            }
            state.stream = null;
        },
        addToCart(state, value) {
            state.cart.items.push(value);
            localStorage.setItem('cart', JSON.stringify(state.cart));
        },
        changeCartOwner(state, value) {
            state.cart.cartOwner = value;
            localStorage.setItem('cart', JSON.stringify(state.cart));
        },
        // ── Loading overlay ──────────────────────────────────────
        showLoading(state, message = '') {
            state.loading = { active: true, message };
        },
        hideLoading(state) {
            state.loading = { active: false, message: '' };
        },
    },
});
