import axios from 'axios';
import { search } from 'core-js/fn/symbol';
// import store from '../store';

function errorHandler(error, reject) {
    console.log(error);
    if (error.response && error.response.data) {
        reject(error.response.data);
    } else {
        reject(error);
    }
}


export default {
    detail(obj) {
        return new Promise(async (resolve, reject) => {
            try {
                const {data} = await axios.get(`sales/${obj.sales_id}`);
                resolve(data);
            } catch (error) {
                errorHandler(error, reject)
            }
        });
    },
    list(obj = {}) {
        return new Promise(async (resolve, reject) => {
            try {
                // const keys = ['page', 'limit', 'sortBy', 'sortDir', 'item_name', 'item_stock', 'item_stock_opr'];
                const keys = ['item_name'];

                let str = '';
                for (const key in obj) {
                    if (keys.indexOf(key) >= 0 && obj[key]) {
                        str += str ? '&' : '?';
                        str += key + '=' + encodeURIComponent(obj[key]);
                    }
                }

                const url = `/sales${str}`;
                const { data } = await axios.get(url);
                // const { meta, list } = data;
                // obj.total = meta.total;            
                // resolve(list);
                resolve(data);
            } catch (error) {
                errorHandler(error, reject);
            }
        });
    },
    remove(obj) {
        return new Promise(async (resolve, reject) => {
            try {
                const resp = await axios.delete(`/sales/${obj.sales_id}`);
                resolve(resp);
            } catch (error) {
                errorHandler(error, reject);
            }
        })
    },
    save(obj) {
        return new Promise(async (resolve, reject) => {
            try {
                const resp = await axios.post('/sales', obj);
                resolve(resp);
            } catch (error) {
                errorHandler(error, reject);
            }
        });
    },
    update(obj) {
        return new Promise(async (resolve, reject) => {
            try {
                const resp = await axios.put(`/sales/${obj.sales_id}`, obj);
                resolve(resp);
            } catch (error) {
                errorHandler(error, reject);
            }
        })
    },
    printStruk(obj) {
        return new Promise(async (resolve, reject) => {
            try {
                const resp = await axios.post('/print-struk', obj);
                resolve(resp);
            } catch (error) {
                errorHandler(error, reject);
            }
        });
    },
    printDebug(obj) {
        return new Promise(async (resolve, reject) => {
            try {
                const resp = await axios.post('/print-debug', obj);
                resolve(resp);
            } catch (error) {
                errorHandler(error, reject);
            }
        });
    },
    printTest() {
        return new Promise(async (resolve, reject) => {
            try {
                const resp = await axios.get('/print-test');
                resolve(resp);
            } catch (error) {
                errorHandler(error, reject);
            }
        });
    },

};