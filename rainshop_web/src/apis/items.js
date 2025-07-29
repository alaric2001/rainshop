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
                const {data} = await axios.get(`items/${obj.item_id}`);
                resolve(data);
            } catch (error) {
                errorHandler(error, reject)
            }
        });
    },
    list(obj = {}) {
        return new Promise(async (resolve, reject) => {
            try {
                // const keys = ['page', 'limit', 'sortBy', 'sortDir', 'menuname', 'categid', 'categname'];

                let str = '';
                // for (const key in obj) {
                //     if (keys.indexOf(key) >= 0 && obj[key]) {
                //         str += str ? '&' : '?';
                //         str += key + '=' + encodeURIComponent(obj[key]);
                //     }
                // }

                const url = `/items${str}`;
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
                const resp = await axios.delete(`/restomenu/${obj.item_id}`);
                resolve(resp);
            } catch (error) {
                errorHandler(error, reject);
            }
        })
    },
    save(obj) {
        return new Promise(async (resolve, reject) => {
            try {
                const resp = await axios.post('/items', obj);
                resolve(resp);
            } catch (error) {
                errorHandler(error, reject);
            }
        });
    },
    search(obj) {
        return new Promise(async (resolve, reject) => {
            try {
                const resp = await axios.post('/items/search', obj);
                resolve(resp);
            } catch (error) {
                errorHandler(error, reject);
            }
        });
    },

};