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
                const keys = ['page', 'limit', 'sortBy', 'sortDir', 'item_name', 'item_stock'];
                // const keys = ['page', 'limit','item_name'];

                let str = '';
                for (const key in obj) {
                    if (keys.indexOf(key) >= 0 && obj[key]) {
                        str += str ? '&' : '?';
                        str += key + '=' + encodeURIComponent(obj[key]);
                    }
                }

                const url = `/items${str}`;
                const { data } = await axios.get(url);
                obj.total = data.total;
                resolve(data.data);
            } catch (error) {
                errorHandler(error, reject);
            }
        });
    },
    remove(obj) {
        return new Promise(async (resolve, reject) => {
            try {
                const resp = await axios.delete(`/items/${obj.item_id}`);
                resolve(resp);
            } catch (error) {
                errorHandler(error, reject);
            }
        })
    },
    insert(obj) {
        return new Promise(async (resolve, reject) => {
            try {
                const resp = await axios.post('/items', obj);
                resolve(resp);
            } catch (error) {
                errorHandler(error, reject);
            }
        });
    },
    update(obj) {
        return new Promise(async (resolve, reject) => {
            try {
                const resp = await axios.put(`/items/${obj.item_id}`, obj);
                resolve(resp);
            } catch (error) {
                errorHandler(error, reject);
            }
        })
    },
    insertImage(obj) {
        return new Promise(async (resolve, reject) => {
            try {
                const resp = await axios.post('/images', obj);
                resolve(resp);
            } catch (error) {
                errorHandler(error, reject);
            }
        });
    },
    updateImage(obj) {
        return new Promise(async (resolve, reject) => {
            try {
                const resp = await axios.put(`/images/${obj.image_id}`, obj);
                resolve(resp);
            } catch (error) {
                errorHandler(error, reject);
            }
        })
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
    imageSearch(obj) {
        return new Promise(async (resolve, reject) => {
            try {
                const {data} = await axios.post('/images/search', obj);
                resolve(data);
            } catch (error) {
                errorHandler(error, reject);
            }
        });
    },
    imageItem(id) {
        return new Promise(async (resolve, reject) => {
            try {
                const {data} = await axios.get(`images/${id}`);
                resolve(data);
            } catch (error) {
                errorHandler(error, reject)
            }
        });
    },

};