import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);


export default new Vuex.Store({
    // namespaced: true,
      state: {
        stream: null,
        cart: { display: 0, items: [], cartOwner: '' }
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
            // console.log('cartOwner : ', value);
            state.cart.cartOwner=value;
            localStorage.setItem('cart', JSON.stringify(state.cart));
        },
    },
    // actions: {
    //     "SOCKET_restonotification"(state, value) {
    //         // console.log('VUEX ACTION, notificationcounter Update from socket', value);
    //         const myNotif = (value || []).reduce((newArr, item) => {
    //             if ((item.outletid === this.state.user.outletid) && (item.compcode === this.state.user.compcode) && (item.notifName)) {
    //                 newArr.push(item);
    //                 if (item.notifName=='Open Order') this.state.openOrder = item.counter;
    //                 if (item.notifName == 'Kitchen Job') this.state.kitchenJob = item.counter;
    //                 if (item.notifName == 'Table Usage') this.state.tableUsage = item.counter;
    //             }
    //             return newArr;
    //         }, []);
    //         this.state.notifications = myNotif;
    //     },
    // }
})
