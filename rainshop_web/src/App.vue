<template>
  <div id="app">
    <router-view></router-view>
    <app-footer fixed >
        <div>
            <nav>
            <router-link to="/input">Input Barang</router-link> |
            <router-link to="/search">Cari Barang</router-link> |
            <router-link to="/penjualan">Penjualan</router-link>
            </nav>
        </div>
        <div class="ml-auto" >
          <i class="fa fa-heart" aria-hidden="true" style="color:red;"></i>
            <strong style="color: #4A2574;" class="ml-1">RAIN-SHOP </strong>        
        </div>        
    </app-footer>
  </div>
</template>


<style lang="scss">
  @import '~@coreui/icons/css/coreui-icons.min.css';
  $fa-font-path: '~font-awesome/fonts/';
  @import '~font-awesome/scss/font-awesome';
  @import '~bootstrap-vue/dist/bootstrap-vue.css';
  @import 'assets/scss/style';
</style>

<script>
import { Footer as AppFooter } from "@coreui/vue";

export default {
  components: { AppFooter},
  data() {
    return { navItems: [] };
  },
};
</script>
