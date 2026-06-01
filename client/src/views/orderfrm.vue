<template>
  <div class="pos-page">

    <!-- Mobile Tab Bar (hanya muncul di layar kecil) -->
    <div class="mobile-tabs d-flex d-md-none">
      <button @click="activeTab='search'" :class="['tab-btn', activeTab==='search' && 'active']">
        <i class="fa fa-search"></i> Cari Barang
      </button>
      <button @click="activeTab='cart'" :class="['tab-btn', activeTab==='cart' && 'active']">
        <i class="fa fa-shopping-cart"></i> Keranjang
        <span v-if="lineorder.length" class="tab-badge">{{ lineorder.length }}</span>
      </button>
    </div>

    <!-- Dua panel: Search (kiri) dan Cart (kanan) -->
    <div class="pos-body">

      <!-- Panel Kiri: Cari Barang -->
      <div class="pos-panel search-panel" v-show="activeTab === 'search' || isDesktop">

        <!-- Search Bar -->
        <div class="panel-header">
          <div class="panel-title">Cari Item Barang</div>
          <div class="search-controls">
            <div class="search-row">
              <b-button variant="success" class="btn-camera" @click="showWebcam=true">
                <i class="fa fa-camera"></i><span class="d-none d-sm-inline"> Kamera</span>
              </b-button>
              <b-input-group class="flex-fill">
                <b-form-input
                  v-model="tblData.item_name"
                  placeholder="Tulis nama barang..."
                  @keyup.13.native="getItems()"
                />
                <b-input-group-append>
                  <b-button variant="outline-secondary" @click="tblData.item_name=''">
                    <i class="fa fa-times"></i>
                  </b-button>
                  <b-button variant="primary" @click="getItems">
                    <i class="fa fa-search"></i>
                  </b-button>
                </b-input-group-append>
              </b-input-group>
            </div>
          </div>
        </div>

        <!-- Daftar Item -->
        <div class="panel-scroll">
          <div v-if="!itemList.length" class="empty-state">
            <i class="fa fa-box-open"></i>
            <p>Cari barang di atas atau gunakan kamera</p>
          </div>
          <b-table
            v-else
            class="item-table mb-0"
            ref="tblHasil"
            hover
            :items="itemList"
            :fields="fields"
            @row-clicked="clickItemDibeli"
          >
            <template v-slot:cell(item_name)="data">
              <div class="item-name">{{ data.item.item_name }}</div>
              <div class="item-meta">
                <span class="item-price">Rp {{ data.item.item_price | numFormat }}</span>
                <span class="item-stock">Stok: {{ data.item.item_stock }}</span>
              </div>
            </template>
            <template v-slot:cell(image1)="data">
              <img
                :src="data.item.image"
                :key="data.item.image"
                @click.stop="openZoomImage(data.item.image)"
                class="item-thumb"
                alt
              />
            </template>
          </b-table>
        </div>
      </div>

      <!-- Panel Kanan: Keranjang & Pembayaran -->
      <div class="pos-panel cart-panel" v-show="activeTab === 'cart' || isDesktop">

        <!-- Cart Header -->
        <div class="panel-header cart-header">
          <span class="panel-title">
            <span v-if="frmdata.totalitem">{{ frmdata.totalitem }} ({{ frmdata.totalqty }})</span>
            <span v-else>Keranjang Belanja</span>
          </span>
          <span v-if="frmdata.sales_no" class="struk-badge">{{ frmdata.sales_no }}</span>
        </div>

        <!-- Daftar Item di Keranjang -->
        <div class="panel-scroll cart-scroll">
          <div v-if="!lineorder.length" class="empty-state">
            <i class="fa fa-shopping-cart"></i>
            <p>Keranjang masih kosong</p>
            <p class="text-muted">Tap item barang untuk menambahkan</p>
          </div>
          <div v-else class="cart-list">
            <div v-for="(m, key) in lineorder" :key="key" class="cart-item">
              <div class="cart-item-info">
                <div class="cart-item-name">{{ m.item_name }}</div>
                <div class="cart-item-price">@ Rp {{ m.item_price | numFormat('0,0') }}</div>
              </div>
              <div class="cart-item-qty">
                <button class="qty-btn minus" @click="decreaseQty(m)"><i class="fa fa-minus"></i></button>
                <span class="qty-val">{{ m.qty }}</span>
                <button class="qty-btn plus" @click="increaseQty(m)"><i class="fa fa-plus"></i></button>
              </div>
              <div class="cart-item-sub">Rp {{ (m.qty * m.item_price) | numFormat('0,0') }}</div>
              <button class="cart-del" @click="deleteItem(m, key)"><i class="fa fa-trash"></i></button>
            </div>
          </div>
        </div>

        <!-- Pembayaran -->
        <div class="payment-area">
          <div class="pay-row total-row">
            <span>Total Belanja</span>
            <span class="pay-total">Rp {{ frmdata.sales_total | numFormat('0,0') }}</span>
          </div>
          <div class="pay-row">
            <span>Cara Bayar</span>
            <b-form-radio-group v-model="frmdata.sales_paym" class="pay-method">
              <b-form-radio value="TUNAI">Tunai</b-form-radio>
              <b-form-radio value="QRIS" class="ml-2">QRIS</b-form-radio>
            </b-form-radio-group>
          </div>
          <div class="pay-row">
            <span>Uang Bayar</span>
            <my-number
              class="form-control text-right pay-input"
              separator=","
              :precision="2"
              v-model="frmdata.paid_amount"
              :state="!$v.frmdata.paid_amount.$error"
            />
          </div>
          <div class="pay-row" v-if="frmdata.paid_amount > 0">
            <span>Kembalian</span>
            <span class="pay-change" :class="{ negative: frmdata.change_amount < 0 }">
              Rp {{ frmdata.change_amount | numFormat('0,0') }}
            </span>
          </div>
          <div class="pay-actions">
            <b-button variant="primary" size="lg" class="btn-print" @click="saveOrder()">
              <i class="fa fa-print"></i> Print Struk
            </b-button>
            <b-button variant="outline-secondary" class="btn-clear" @click="clearForm()">
              <i class="fa fa-refresh"></i> Kosongkan
            </b-button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Kamera -->
    <b-modal v-model="showWebcam" title="Cari Barang dengan Kamera" size="lg" :centered="true" hide-footer>
      <CameraCapture @image-captured="searchItem" class="mb-2"/>
    </b-modal>

    <!-- Modal Zoom Gambar -->
    <b-modal v-model="showZoomGambar" title="Zoom Gambar" size="md" :centered="true" ok-only>
      <img :src="zoomImage" :key="zoomImage" class="img-fluid" alt />
    </b-modal>

  </div>
</template>

<style lang="scss" scoped>
// ── Layout utama ──────────────────────────────────────────────
.pos-page {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 56px); // tinggi dikurangi bottom-nav
  background: #f1f5f9;
  padding: 8px;
  gap: 8px;
  overflow: hidden;
}

// ── Mobile Tab Bar ────────────────────────────────────────────
.mobile-tabs {
  flex-shrink: 0;
  background: #fff;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,.06);
}

.tab-btn {
  flex: 1;
  padding: 10px 8px;
  border: none;
  background: transparent;
  font-weight: 500;
  color: #64748b;
  font-size: 14px;
  cursor: pointer;
  transition: all .2s;
  position: relative;

  &.active {
    background: #2563eb;
    color: #fff;
  }

  .tab-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: #ef4444;
    color: #fff;
    border-radius: 50%;
    width: 18px;
    height: 18px;
    font-size: 11px;
    margin-left: 4px;
    font-weight: 700;
  }
}

// ── Pos Body (flex row) ───────────────────────────────────────
.pos-body {
  flex: 1;
  display: flex;
  gap: 10px;
  overflow: hidden;
  min-height: 0;

  @media (max-width: 767px) {
    // pada mobile hanya 1 panel yang tampil (dikontrol v-show)
    flex-direction: column;
  }
}

// ── Panel generik ─────────────────────────────────────────────
.pos-panel {
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,.06);
  min-height: 0;

  &.search-panel { flex: 7; }
  &.cart-panel   { flex: 5; }

  @media (max-width: 767px) {
    &.search-panel,
    &.cart-panel {
      flex: 1;
    }
  }
}

// ── Panel Header ──────────────────────────────────────────────
.panel-header {
  padding: 10px 14px;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
  flex-shrink: 0;
}

.panel-title {
  font-size: 12px;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: .05em;
  margin-bottom: 8px;
  display: block;
}

.search-row {
  display: flex;
  gap: 8px;
  align-items: center;

  .btn-camera {
    flex-shrink: 0;
    height: 38px;
  }

  .flex-fill { flex: 1; min-width: 0; }
}

// ── Scrollable area ───────────────────────────────────────────
.panel-scroll {
  flex: 1;
  overflow-y: auto;
  min-height: 0;

  -webkit-overflow-scrolling: touch;
}

// ── Item Table ────────────────────────────────────────────────
.item-table {
  ::v-deep thead th {
    background: #f8fafc !important;
    color: #475569 !important;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .04em;
    border-bottom: 2px solid #e2e8f0 !important;
    padding: 8px 12px;
  }

  ::v-deep tbody tr {
    cursor: pointer;
    &:hover { background: #eff6ff !important; }
    &:active { background: #dbeafe !important; }
    td { padding: 10px 12px; vertical-align: middle; }
  }
}

.item-name {
  font-weight: 600;
  font-size: 15px;
  color: #1e293b;
  line-height: 1.3;
}

.item-meta {
  display: flex;
  gap: 12px;
  margin-top: 3px;
  flex-wrap: wrap;
}

.item-price {
  color: #2563eb;
  font-weight: 600;
  font-size: 13px;
}

.item-stock {
  color: #64748b;
  font-size: 12px;
}

.item-thumb {
  width: 70px;
  height: 70px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  cursor: zoom-in;
  display: block;
}

// ── Empty State ───────────────────────────────────────────────
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 160px;
  color: #94a3b8;
  text-align: center;
  padding: 24px;

  i { font-size: 36px; margin-bottom: 10px; }
  p { margin: 2px 0; font-size: 14px; }
}

// ── Cart Header ───────────────────────────────────────────────
.cart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .panel-title { margin: 0; }
}

.struk-badge {
  font-size: 11px;
  background: #e2e8f0;
  color: #475569;
  padding: 2px 8px;
  border-radius: 20px;
  font-weight: 600;
}

// ── Cart List ─────────────────────────────────────────────────
.cart-scroll { padding: 6px 0; }

.cart-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-bottom: 1px solid #f1f5f9;
  transition: background .15s;

  &:last-child { border-bottom: none; }
  &:hover { background: #f8fafc; }
}

.cart-item-info {
  flex: 1;
  min-width: 0;

  .cart-item-name {
    font-size: 13px;
    font-weight: 600;
    color: #1e293b;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .cart-item-price {
    font-size: 11px;
    color: #64748b;
    margin-top: 1px;
  }
}

.cart-item-qty {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}

.qty-btn {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  background: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  transition: all .15s;

  &.minus { color: #ef4444; &:hover { border-color: #ef4444; background: #fef2f2; } }
  &.plus  { color: #16a34a; &:hover { border-color: #16a34a; background: #f0fdf4; } }

  &:active { transform: scale(.92); }
}

.qty-val {
  font-weight: 700;
  font-size: 15px;
  min-width: 22px;
  text-align: center;
  color: #1e293b;
}

.cart-item-sub {
  font-weight: 600;
  font-size: 13px;
  color: #2563eb;
  min-width: 80px;
  text-align: right;
  flex-shrink: 0;
}

.cart-del {
  background: none;
  border: none;
  color: #cbd5e1;
  cursor: pointer;
  padding: 4px;
  transition: color .15s;
  flex-shrink: 0;

  &:hover { color: #ef4444; }
}

// ── Payment Area ──────────────────────────────────────────────
.payment-area {
  border-top: 2px solid #e2e8f0;
  padding: 12px 14px;
  background: #f8fafc;
  flex-shrink: 0;
}

.pay-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 13px;
  color: #475569;
  font-weight: 500;
  gap: 8px;
}

.total-row {
  font-size: 15px;
  font-weight: 700;
  color: #1e293b;
  padding-bottom: 8px;
  margin-bottom: 8px;
  border-bottom: 1px solid #e2e8f0;
}

.pay-total {
  font-size: 18px;
  font-weight: 800;
  color: #2563eb;
}

.pay-change {
  font-size: 16px;
  font-weight: 700;
  color: #16a34a;

  &.negative { color: #ef4444; }
}

.pay-method {
  display: flex;
  gap: 4px;
  font-size: 13px;
}

.pay-input {
  max-width: 140px;
  font-weight: 600;
  font-size: 14px;
}

.pay-actions {
  display: flex;
  gap: 8px;
  margin-top: 10px;

  .btn-print {
    flex: 1;
    font-weight: 700;
    font-size: 15px;
  }

  .btn-clear {
    flex-shrink: 0;
    font-size: 13px;
  }
}
</style>

<script>
import CameraCapture from "../components/CameraCapture.vue";
import items from "../apis/items";
import sales from "../apis/sales";
import moment from 'moment';
import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'
import myNumber from "../components/my-number";
import toastr from "mini-toastr";
toastr.init();

export default {
  components: { myNumber, CameraCapture },
  mixins: [validationMixin],
  validations: {
    frmdata: {
      paid_amount: { required },
    },
  },
  data() {
    return {
      activeTab: 'search',
      isDesktop: window.innerWidth >= 768,
      itemsApi: items,
      showWebcam: false,
      fields: [
        { key: "item_name", label: "Nama Item Barang", sortable: true },
        { key: "image1", thStyle: "width:90px", label: "Foto", tdClass: "text-center" },
      ],
      frmdata: {
        sales_id: '', sales_no: '', paid_amount: 0,
        totalitem: '', sales_total: 0, change_amount: 0, sales_paym: 'TUNAI'
      },
      selectedItem: null,
      itemList: [],
      lineorder: [],
      tblData: {
        page: 1, limit: 10, total: 0,
        sortBy: null, sortDesc: false, item_name: ''
      },
      modeViewOnly: false,
      zoomImage: null,
      showZoomGambar: false,
    };
  },
  created() {
    this.$watch('frmdata.paid_amount', function(newval) {
      this.frmdata.change_amount = parseFloat(newval || 0) - parseFloat(this.frmdata.sales_total || 0);
    });
    window.addEventListener('resize', this.onResize);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.onResize);
  },
  methods: {
    onResize() {
      this.isDesktop = window.innerWidth >= 768;
    },
    async searchItem(imageData) {
      try {
        const list = await items.imageSearch({ image: imageData });
        list.forEach(el => {
          el.image = '';
          items.imageItem(el.image_id).then(img => { el.image = img; });
        });
        this.itemList = list;
        this.showWebcam = false;
        if (!this.isDesktop) this.activeTab = 'search';
      } catch (error) {
        console.error(error);
        toastr.error("Gagal mencari item!");
      }
    },
    async getItems() {
      const list = await items.list(this.tblData);
      list.forEach(el => {
        el.image = '';
        items.imageItem(el.image_id).then(img => { el.image = img; });
      });
      this.itemList = list;
    },
    clickItemDibeli(menu) {
      this.selectedItem = {};
      for (const key in menu) this.selectedItem[key] = menu[key];
      this.selectedItem.qty = 1;
      this.lineorder.push(this.selectedItem);
      this.hitungTotal();
      if (!this.isDesktop) this.activeTab = 'cart';
    },
    increaseQty(row) {
      row.qty += 1;
      this.hitungTotal();
    },
    decreaseQty(row) {
      if (row.qty > 1) row.qty -= 1;
      this.hitungTotal();
    },
    deleteItem(item, idx) {
      this.selectedItem = null;
      this.lineorder.splice(idx, 1);
      this.hitungTotal();
    },
    hitungTotal() {
      let totalqty = 0, subtotal = 0;
      this.lineorder.forEach(item => {
        item.subtotal = item.qty * item.item_price;
        subtotal += item.subtotal;
        totalqty += item.qty;
      });
      this.frmdata.totalitem = `${this.lineorder.length} ${this.lineorder.length > 1 ? 'items' : 'item'}`;
      this.frmdata.totalqty = `${totalqty} Qty`;
      this.frmdata.subtotal = subtotal;
      this.frmdata.sales_total = subtotal;
      if (this.frmdata.paid_amount) {
        this.frmdata.change_amount = parseFloat(this.frmdata.paid_amount) - parseFloat(subtotal);
      }
      this.$forceUpdate();
    },
    async saveOrder() {
      try {
        this.hitungTotal();
        const data = {};
        const keys = ['sales_id','sales_no','sales_total','sales_paym','totalitem','paid_amount','change_amount'];
        for (const key in this.frmdata) {
          if (keys.indexOf(key) >= 0 && this.frmdata[key]) data[key] = this.frmdata[key];
        }
        const keysLine = ['sales_id','sales_line_id','item_id','item_price','qty','subtotal','item_name'];
        data.lines = this.lineorder.reduce((arr, item) => {
          const newitem = {};
          for (const key in item) {
            if (keysLine.indexOf(key) >= 0 && item[key]) newitem[key] = item[key];
          }
          arr.push(newitem);
          return arr;
        }, []);

        const baru = !this.frmdata.sales_id;
        sales.printStruk(data);
        const result = await sales.save(data);
        this.frmdata.sales_id = result.data.sales_id;
        this.frmdata.sales_no = result.data.sales_no;
        data.sales_id = result.data.sales_id;
        data.sales_no = result.data.sales_no;
        toastr.success(baru ? `Tersimpan. No: ${this.frmdata.sales_no}` : 'Perubahan tersimpan');
      } catch (error) {
        console.error(error);
        const msg = error.message || error.sqlMessage || JSON.stringify(error);
        toastr.error(msg, 'ERROR', 10000);
      }
    },
    openZoomImage(gambar) {
      this.zoomImage = gambar;
      this.showZoomGambar = true;
    },
    clearForm() {
      for (const key in this.frmdata) this.frmdata[key] = '';
      this.frmdata.sales_paym = 'TUNAI';
      this.frmdata.paid_amount = 0;
      this.frmdata.sales_total = 0;
      this.frmdata.change_amount = 0;
      this.lineorder = [];
      this.hitungTotal();
    },
  },
};
</script>
