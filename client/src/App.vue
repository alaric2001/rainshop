<template>
  <div id="app">
    <router-view></router-view>
    <GlobalLoader />
    <nav class="bottom-nav">
      <router-link to="/item-input" class="nav-item" active-class="active">
        <i class="fa fa-plus-circle"></i>
        <span>Input Barang</span>
      </router-link>
      <router-link to="/item-list" class="nav-item" active-class="active">
        <i class="fa fa-list"></i>
        <span>Daftar Barang</span>
      </router-link>
      <router-link to="/search" class="nav-item" active-class="active">
        <i class="fa fa-search"></i>
        <span>Cari Barang</span>
      </router-link>
      <router-link to="/penjualan" class="nav-item" active-class="active">
        <i class="fa fa-shopping-cart"></i>
        <span>Penjualan</span>
      </router-link>
    </nav>
  </div>
</template>

<style lang="scss">
  @import '~@coreui/icons/css/coreui-icons.min.css';
  $fa-font-path: '~font-awesome/fonts/';
  @import '~font-awesome/scss/font-awesome';
  @import '~bootstrap-vue/dist/bootstrap-vue.css';
  @import 'assets/scss/style';

  * { box-sizing: border-box; }

  #app {
    padding-bottom: 56px;
  }

  .bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 56px;
    background: #ffffff;
    border-top: 1px solid #e2e8f0;
    display: flex;
    align-items: stretch;
    z-index: 9999;
    box-shadow: 0 -2px 8px rgba(0,0,0,.08);

    .nav-item {
      flex: 1;
      min-width: 0;           // cegah overflow flex item
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 2px;
      color: #94a3b8;
      text-decoration: none;
      font-size: 9px;
      font-weight: 500;
      transition: color .15s;
      padding: 0 2px;
      overflow: hidden;       // cegah teks keluar dari kotak

      i {
        font-size: 17px;
        line-height: 1;
        flex-shrink: 0;
      }

      span {
        line-height: 1.2;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
      }

      &.active {
        color: #2563eb;
      }

      &:hover {
        color: #2563eb;
        background: #f8fafc;
        text-decoration: none;
      }
    }
  }
</style>

<script>
import GlobalLoader from './components/GlobalLoader.vue';

export default {
  components: { GlobalLoader },
  data() {
    return { navItems: [] };
  },
};
</script>
