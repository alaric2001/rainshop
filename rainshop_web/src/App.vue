<template>
  <div id="app">
    <nav>
      <router-link to="/input">Input Barang</router-link> |
      <router-link to="/search">Cari Barang</router-link>
    </nav>
    <router-view></router-view>
  </div>
</template>


<style lang="scss">
  @import '~@coreui/icons/css/coreui-icons.min.css';
  $fa-font-path: '~font-awesome/fonts/';
  @import '~font-awesome/scss/font-awesome';
  @import '~bootstrap-vue/dist/bootstrap-vue.css';
  @import 'assets/scss/style';
</style>
