<template>
  <div class="item-form-page">

    <div class="page-header">
      <h6 class="page-title">Input Item Barang Baru</h6>
    </div>

    <div class="form-body">

      <!-- Kolom Kiri: Kamera + Foto -->
      <div class="form-col col-camera">

        <!-- Section: Kamera -->
        <div class="form-section">
          <div class="section-label">
            <span class="step-num">1</span> Ambil Foto Barang
          </div>
          <div class="camera-wrapper">
            <CameraCapture3
              :key="resetCamera"
              @image-captured="handleImageCaptured"
              @image2-captured="handleImage2Captured"
              @image3-captured="handleImage3Captured"
            />
          </div>
          <b-button
            v-if="capturedImage && searchResults.length === 0"
            variant="outline-warning"
            size="sm"
            class="mt-2 w-100"
            @click="searchItem"
          >
            <i class="fa fa-search"></i> Cek — apakah sudah pernah didaftarkan?
          </b-button>
        </div>

        <!-- Section: Hasil pencarian duplikat -->
        <div v-if="searchResults.length" class="form-section">
          <div class="section-label text-warning">
            <i class="fa fa-exclamation-triangle"></i> Gambar ini mirip dengan barang berikut:
          </div>
          <div v-for="item in searchResults" :key="item.item_id" class="similar-item">
            <img
              v-if="item.image"
              :src="item.image"
              class="similar-thumb"
              @click="openZoomImage(item.image)"
              alt
            />
            <div class="similar-info">
              <div class="similar-name">{{ item.item_name }}</div>
              <div class="similar-price">Rp {{ item.item_price | numFormat }}</div>
              <div v-if="item.modified" class="similar-date">
                {{ item.modified | moment("DD MMM YYYY") }}
              </div>
            </div>
            <b-button variant="outline-primary" size="sm" @click="rowEditGambar(item)">
              Edit
            </b-button>
          </div>
        </div>

        <!-- Section: Preview Foto -->
        <div v-if="capturedImage || capturedImage2 || capturedImage3" class="form-section">
          <div class="section-label">
            <span class="step-num">2</span> Preview Foto
          </div>
          <div class="image-grid">
            <div v-if="capturedImage" class="image-preview-card">
              <img :src="capturedImage" alt="Gambar#1" @click="openZoomImage(capturedImage)" />
              <div class="image-label">
                Foto #1
                <button class="img-del" @click="capturedImage=null">
                  <i class="fa fa-times"></i>
                </button>
              </div>
            </div>
            <div v-if="capturedImage2" class="image-preview-card">
              <img :src="capturedImage2" alt="Gambar#2" @click="openZoomImage(capturedImage2)" />
              <div class="image-label">
                Foto #2
                <button class="img-del" @click="capturedImage2=null">
                  <i class="fa fa-times"></i>
                </button>
              </div>
            </div>
            <div v-if="capturedImage3" class="image-preview-card">
              <img :src="capturedImage3" alt="Gambar#3" @click="openZoomImage(capturedImage3)" />
              <div class="image-label">
                Foto #3
                <button class="img-del" @click="capturedImage3=null">
                  <i class="fa fa-times"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Kolom Kanan: Form Data Barang -->
      <div class="form-col col-form">
        <div class="form-section">
          <div class="section-label">
            <span class="step-num">3</span> Data Barang
          </div>

          <div class="field-group">
            <label class="field-label">Nama Barang <span class="required">*</span></label>
            <b-form-input
              v-model="model.item_name"
              placeholder="Nama item barang..."
              :state="$v.model.item_name.$dirty ? !$v.model.item_name.$error : null"
            />
          </div>

          <div class="field-row">
            <div class="field-group">
              <label class="field-label">Harga Jual <span class="required">*</span></label>
              <my-number
                class="form-control text-right"
                separator=","
                :precision="0"
                v-model="model.item_price"
                :state="$v.model.item_price.$dirty ? !$v.model.item_price.$error : null"
              />
            </div>
            <div class="field-group">
              <label class="field-label">Jumlah Stok <span class="required">*</span></label>
              <b-form-input
                v-model="model.item_stock"
                type="number"
                :min="1"
                :state="$v.model.item_stock.$dirty ? !$v.model.item_stock.$error : null"
              />
            </div>
          </div>

          <div class="form-actions">
            <b-button variant="success" class="btn-save" @click="submitItem">
              <i class="fa fa-save"></i> Simpan Barang
            </b-button>
            <b-button variant="outline-secondary" class="btn-reset" @click="resetForm">
              <i class="fa fa-refresh"></i> Reset
            </b-button>
          </div>
        </div>
      </div>

    </div>

    <!-- Modal zoom gambar -->
    <b-modal v-model="showZoomGambar" title="Zoom Gambar" size="md" :centered="true" ok-only>
      <img :src="zoomImage" :key="zoomImage" class="img-fluid" alt />
    </b-modal>

    <!-- Modal edit gambar barang yang sudah ada -->
    <b-modal v-model="showEditGambar" title="Edit Gambar Barang" size="lg" :centered="true" hide-footer>
      <div class="edit-gambar-modal">
        <div class="field-group mb-3">
          <label class="field-label">Nama Barang</label>
          <b-form-input v-model="frmdata.item_name" disabled />
        </div>
        <div class="field-row mb-3">
          <div class="field-group">
            <label class="field-label">Harga</label>
            <my-number class="form-control text-right" separator="," :precision="0" v-model="frmdata.item_price" />
          </div>
          <div class="field-group">
            <label class="field-label">Stok</label>
            <b-form-input v-model="frmdata.item_stock" type="number" :min="1" />
          </div>
        </div>
        <div class="d-flex gap-2 mb-3">
          <b-button variant="success" @click="submitEdit"><i class="fa fa-save"></i> Simpan Data</b-button>
          <b-button variant="outline-secondary" @click="closeEditGambar">Tutup</b-button>
        </div>

        <!-- Mode: lihat gambar -->
        <div v-if="!modeCaptureCamera">
          <div class="section-label mb-2">Gambar Barang</div>
          <div class="image-grid">
            <div v-for="(row, imgIdx) in images" :key="imgIdx" class="image-preview-card">
              <img v-if="row.image" :src="row.image" :key="row.image" class="w-100" alt />
              <div v-else class="no-image-placeholder">
                <i class="fa fa-image"></i>
              </div>
              <div class="image-label">
                Foto #{{ imgIdx + 1 }}
                <button class="img-edit" @click="ShowCaptureCamera(imgIdx)">
                  <i class="fa fa-camera"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Mode: kamera untuk edit gambar -->
        <div v-else>
          <div class="section-label mb-2">Ambil Foto Baru untuk Foto #{{ editImageIdx + 1 }}</div>
          <div class="edit-camera-row">
            <div class="edit-camera-feed">
              <CameraCapture @image-captured="handleImageCaptured" />
            </div>
            <div class="edit-camera-preview">
              <img v-if="capturedImage" :src="capturedImage" class="w-100" alt="Preview" />
              <div v-else class="no-image-placeholder"><i class="fa fa-camera"></i><p>Belum ada foto</p></div>
              <div class="d-flex gap-2 mt-2">
                <b-button variant="success" size="sm" @click="submitEditGambar">
                  <i class="fa fa-save"></i> Simpan Foto
                </b-button>
                <b-button variant="outline-secondary" size="sm" @click="modeCaptureCamera=false">
                  Batal
                </b-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </b-modal>

  </div>
</template>

<style lang="scss" scoped>
.item-form-page {
  padding: 8px;
  min-height: calc(100vh - 56px);
  background: #f1f5f9;
}

.page-header {
  padding: 10px 4px 8px;
}

.page-title {
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

// ── Layout dua kolom ──────────────────────────────────────────
.form-body {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  flex-wrap: wrap;

  @media (max-width: 767px) {
    flex-direction: column;
  }
}

.form-col {
  min-width: 0;

  &.col-camera {
    flex: 1 1 340px;
  }

  &.col-form {
    flex: 1 1 280px;
  }

  @media (max-width: 767px) {
    width: 100%;
    flex: none;
  }
}

// ── Section ───────────────────────────────────────────────────
.form-section {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 14px;
  margin-bottom: 10px;
  box-shadow: 0 1px 3px rgba(0,0,0,.05);
}

.section-label {
  font-size: 12px;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: .05em;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.step-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #2563eb;
  color: #fff;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 11px;
  font-weight: 700;
  flex-shrink: 0;
}

// ── Kamera ────────────────────────────────────────────────────
// Wrapper hanya sebagai container — video-box dan styling ada di dalam komponen CameraCapture3
.camera-wrapper {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
}

// ── Image grid ────────────────────────────────────────────────
.image-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;

  @media (max-width: 400px) {
    grid-template-columns: repeat(2, 1fr);
  }
}

.image-preview-card {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
  background: #f8fafc;

  img {
    width: 100%;
    aspect-ratio: 1;
    object-fit: cover;
    display: block;
    cursor: zoom-in;
  }

  .image-label {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 4px 8px;
    font-size: 11px;
    font-weight: 600;
    color: #475569;
    background: #f1f5f9;
  }
}

.img-del, .img-edit {
  background: none;
  border: none;
  cursor: pointer;
  padding: 2px;
  font-size: 12px;
  line-height: 1;
}

.img-del  { color: #ef4444; &:hover { color: #b91c1c; } }
.img-edit { color: #2563eb; &:hover { color: #1d4ed8; } }

.no-image-placeholder {
  width: 100%;
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #cbd5e1;
  font-size: 24px;
  gap: 4px;
  p { font-size: 10px; margin: 0; }
}

// ── Duplikat hasil cari ───────────────────────────────────────
.similar-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid #f1f5f9;

  &:last-child { border-bottom: none; }
}

.similar-thumb {
  width: 52px;
  height: 52px;
  object-fit: cover;
  border-radius: 8px;
  cursor: zoom-in;
  flex-shrink: 0;
  border: 1px solid #e2e8f0;
}

.similar-info {
  flex: 1;
  min-width: 0;
  .similar-name  { font-weight: 600; font-size: 13px; color: #1e293b; }
  .similar-price { font-size: 12px; color: #2563eb; }
  .similar-date  { font-size: 11px; color: #94a3b8; }
}

// ── Form fields ───────────────────────────────────────────────
.field-group {
  margin-bottom: 10px;
}

.field-label {
  font-size: 12px;
  font-weight: 600;
  color: #475569;
  margin-bottom: 4px;
  display: block;
  .required { color: #ef4444; }
}

.field-row {
  display: flex;
  gap: 10px;

  .field-group { flex: 1; }

  @media (max-width: 360px) {
    flex-direction: column;
  }
}

.form-actions {
  display: flex;
  gap: 8px;
  margin-top: 14px;

  .btn-save  { flex: 1; font-weight: 700; }
  .btn-reset { flex-shrink: 0; }
}

// ── Modal edit gambar ─────────────────────────────────────────
.edit-gambar-modal {
  .gap-2 { gap: 8px; }
}

.edit-camera-row {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;

  .edit-camera-feed,
  .edit-camera-preview {
    flex: 1 1 200px;
    min-width: 0;
  }

  .edit-camera-feed ::v-deep video {
    width: 100% !important;
    height: auto !important;
  }
}
</style>

<script>
import items from "../apis/items";
import Loading from 'vue-loading-overlay';
import myNumber from "../components/my-number";
import CameraCapture from "../components/CameraCapture2.vue";
import CameraCapture3 from "../components/CameraCapture3.vue";
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";
import toastr from "mini-toastr";
toastr.init();

export default {
  components: { Loading, myNumber, CameraCapture, CameraCapture3 },
  mixins: [validationMixin],
  validations: {
    model: {
      item_name: { required },
      item_price: { required },
      item_stock: { required },
    },
    frmdata: {
      item_name: { required },
      item_price: { required },
      item_stock: { required },
    },
  },
  data() {
    return {
      itemsApi: items,
      isLoading: false,
      resetCamera: false,
      model: { item_name: '', item_price: 0, item_stock: 1 },
      frmdata: { item_name: '', item_price: 0, item_stock: 1 },
      capturedImage: null,
      capturedImage2: null,
      capturedImage3: null,
      searchResults: [],
      fields: [
        { key: "item_name", label: "Nama yg pernah didaftarkan" },
        { key: "image", thStyle: "width:80px", label: "Gambar", thClass: "text-center", tdClass: "text-center" },
        { key: "modified", label: "Tgl", thStyle: "width:80px", thClass: "text-center", tdClass: "text-center" },
      ],
      images: [],
      zoomImage: null,
      showZoomGambar: false,
      showEditGambar: false,
      modeCaptureCamera: false,
      editImageIdx: null,
    };
  },
  methods: {
    handleImageCaptured(imageData) {
      this.capturedImage = imageData;
      this.searchResults = [];
    },
    handleImage2Captured(imageData) { this.capturedImage2 = imageData; },
    handleImage3Captured(imageData) { this.capturedImage3 = imageData; },
    openZoomImage(gambar) {
      this.zoomImage = gambar;
      this.showZoomGambar = true;
    },
    async searchItem() {
      try {
        const list = await items.imageSearch({ image: this.capturedImage });
        list.forEach(el => {
          el.image = '';
          items.imageItem(el.image_id).then(img => { el.image = img; });
        });
        this.searchResults = list;
      } catch (error) {
        console.error(error);
        toastr.error("Gagal mencari item!");
      }
    },
    async rowEditGambar(record) {
      try {
        this.frmdata.item_id = record.item_id;
        this.frmdata.item_name = record.item_name;
        this.frmdata.item_price = record.item_price;
        this.frmdata.item_stock = record.item_stock;
        const dataSvr = await items.detail(record);
        this.images = dataSvr.images;
        for (let i = 0; i < this.images.length; i++) {
          this.images[i].image = await items.imageItem(this.images[i].image_id);
        }
        while (this.images.length < 3) this.images.push({});
        this.modeCaptureCamera = false;
        this.editImageIdx = null;
        this.showEditGambar = true;
      } catch (error) {
        const msg = error.message || JSON.stringify(error);
        toastr.error(msg, 'ERROR', 10000);
      }
    },
    ShowCaptureCamera(imageIdx) {
      this.editImageIdx = imageIdx;
      this.capturedImage = null;
      this.modeCaptureCamera = true;
    },
    async submitEdit() {
      try {
        await items.update({ ...this.frmdata });
        toastr.success("Data barang berhasil disimpan!");
      } catch (error) {
        toastr.error(error.message || "Gagal menyimpan!", 'ERROR', 10000);
      }
    },
    async submitEditGambar() {
      try {
        if (!this.capturedImage) {
          toastr.error("Ambil foto dulu sebelum simpan", 'ERROR', 10000);
          return;
        }
        const editedImage = this.images[this.editImageIdx];
        const frm = { image: this.capturedImage };
        if (editedImage.image_id) {
          frm.image_id = editedImage.image_id;
          await items.updateImage(frm);
        } else {
          frm.item_id = this.frmdata.item_id;
          const hasil = await items.insertImage(frm);
          editedImage.image_id = hasil.data.image_id;
        }
        editedImage.image = this.capturedImage;
        toastr.success("Foto berhasil disimpan!");
        this.modeCaptureCamera = false;
      } catch (error) {
        toastr.error(error.message || "Gagal menyimpan foto!", 'ERROR', 10000);
      }
    },
    closeEditGambar() { this.showEditGambar = false; },
    async submitItem() {
      this.$v.model.$touch();
      if (this.$v.model.$invalid) {
        toastr.error("Lengkapi data barang terlebih dahulu", 'ERROR', 10000);
        return;
      }
      if (!this.capturedImage && !this.capturedImage2 && !this.capturedImage3) {
        toastr.error('Minimal ambil satu foto barang', 'ERROR', 10000);
        return;
      }
      try {
        const frm = { ...this.model, image: this.capturedImage, image2: this.capturedImage2, image3: this.capturedImage3 };
        await items.insert(frm);
        toastr.success("Item berhasil disimpan!");
        this.resetForm();
      } catch (error) {
        const msg = error.message || error.sqlMessage || JSON.stringify(error);
        toastr.error(msg, 'ERROR', 10000);
      }
    },
    resetForm() {
      this.model = { item_name: '', item_price: 0, item_stock: 1 };
      this.capturedImage = null;
      this.capturedImage2 = null;
      this.capturedImage3 = null;
      this.searchResults = [];
      this.$v.$reset();
    },
  },
};
</script>
