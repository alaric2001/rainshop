<template>
  <div class="search-page">

    <div class="page-header">
      <h6 class="page-title"><i class="fa fa-search"></i> Cari Barang dengan Kamera</h6>
    </div>

    <!-- Layout dua kolom — sama dengan item-form.vue -->
    <div class="search-body">

      <!-- Kolom Kiri: Kamera -->
      <div class="search-col col-camera">
        <div class="form-section">
          <div class="section-label">
            <span class="step-num"><i class="fa fa-camera"></i></span>
            Ambil Foto Barang
          </div>

          <!-- ── DESKTOP: webcam live preview ── -->
          <template v-if="!isMobile">
            <div class="camera-wrapper">
              <video ref="video" autoplay muted playsinline></video>
              <canvas ref="canvas" style="display:none;"></canvas>
            </div>
            <b-button
              variant="primary"
              size="lg"
              class="btn-capture w-100 mt-2"
              @click="captureDesktop"
              :disabled="!cameraReady"
            >
              <i class="fa fa-camera"></i>
              {{ cameraReady ? 'Ambil Foto & Cari' : 'Membuka kamera...' }}
            </b-button>
            <div v-if="cameraError" class="camera-error">
              <i class="fa fa-exclamation-triangle"></i> {{ cameraError }}
            </div>
          </template>

          <!-- ── MOBILE: kamera bawaan via file input ── -->
          <template v-else>
            <div class="preview-box" @click="openCamera">
              <img v-if="capturedImage" :src="capturedImage" class="preview-img" alt="Foto barang" />
              <div v-else class="preview-placeholder">
                <i class="fa fa-camera"></i>
                <span>Tap untuk buka kamera</span>
              </div>
            </div>
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              capture="environment"
              style="display:none;"
              @change="onFileChange"
            />
            <b-button
              variant="primary"
              size="lg"
              class="btn-capture w-100 mt-2"
              @click="openCamera"
            >
              <i class="fa fa-camera"></i>
              {{ capturedImage ? 'Ambil Foto Baru' : 'Buka Kamera & Cari' }}
            </b-button>
          </template>

          <div v-if="searching" class="searching-state mt-2">
            <div class="spinner"></div>
            <span>Mencari barang serupa...</span>
          </div>
        </div>
      </div>

      <!-- Kolom Kanan: Hasil -->
      <div class="search-col col-results">

        <div v-if="!shotTaken" class="form-section empty-hint">
          <i class="fa fa-arrow-left d-none d-md-inline"></i>
          <i class="fa fa-arrow-up d-inline d-md-none"></i>
          Foto barang lalu sistem akan mencari yang mirip
        </div>

        <div v-else-if="!searching && searchResults.length === 0" class="form-section empty-result">
          <i class="fa fa-search"></i>
          <p>Tidak ada barang yang cocok</p>
          <p class="text-muted small">Coba foto lebih dekat dan terang</p>
        </div>

        <div v-else-if="searchResults.length" class="form-section results-section">
          <div class="section-label">
            Hasil Pencarian
            <span class="results-count">{{ searchResults.length }} barang</span>
          </div>
          <div class="results-list">
            <div v-for="item in searchResults" :key="item.item_id" class="result-card">
              <div class="result-images">
                <img
                  v-for="(img, idx) in getImages(item)"
                  :key="idx"
                  :src="img"
                  class="result-thumb"
                  @click="openZoom(img)"
                  alt
                />
              </div>
              <div class="result-info">
                <div class="result-name">{{ item.item_name }}</div>
                <div class="result-price">Rp {{ item.item_price | numFormat }}</div>
                <div class="result-meta">
                  <span class="result-stock">Stok: {{ item.item_stock }}</span>
                  <span :class="['result-status', item.isactive ? 'active' : 'inactive']">
                    {{ item.isactive ? 'Aktif' : 'Nonaktif' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <b-modal v-model="showZoom" title="Zoom Gambar" size="md" :centered="true" ok-only>
      <img :src="zoomImage" class="img-fluid" alt />
    </b-modal>

  </div>
</template>

<style lang="scss" scoped>
.search-page {
  padding: 8px;
  min-height: calc(100vh - 56px);
  background: #f1f5f9;
}

.page-header { padding: 10px 4px 8px; }
.page-title {
  font-weight: 700; color: #1e293b; margin: 0;
  i { margin-right: 6px; color: #2563eb; }
}

.search-body {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  flex-wrap: wrap;
  @media (max-width: 767px) { flex-direction: column; }
}

.search-col {
  min-width: 0;
  &.col-camera  { flex: 1 1 340px; }
  &.col-results { flex: 1 1 280px; }
  @media (max-width: 767px) { width: 100%; flex: none; }
}

.form-section {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 14px;
  margin-bottom: 10px;
  box-shadow: 0 1px 3px rgba(0,0,0,.05);
}

.section-label {
  font-size: 12px; font-weight: 700; color: #64748b;
  text-transform: uppercase; letter-spacing: .05em;
  margin-bottom: 10px; display: flex; align-items: center; gap: 6px;
}

.step-num {
  display: inline-flex; align-items: center; justify-content: center;
  background: #2563eb; color: #fff; border-radius: 50%;
  width: 20px; height: 20px; font-size: 11px; font-weight: 700; flex-shrink: 0;
}

// ── Kamera (desktop + mobile) ─────────────────────────────────
// Desktop: live video
.camera-wrapper {
  width: 100%; aspect-ratio: 16/9;
  background: #0f172a; border-radius: 8px; overflow: hidden;
  video { width: 100%; height: 100%; object-fit: cover; display: block; }
}

// Mobile: preview foto
.preview-box {
  width: 100%; aspect-ratio: 16/9;
  background: #0f172a; border-radius: 8px; overflow: hidden;
  cursor: pointer; display: flex; align-items: center; justify-content: center;
}
.preview-img { width: 100%; height: 100%; object-fit: cover; display: block; }
.preview-placeholder {
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  color: #64748b; font-size: 13px;
  i { font-size: 36px; color: #334155; }
}

.camera-error { margin-top: 8px; color: #ef4444; font-size: 13px; text-align: center; }
.btn-capture { font-weight: 700; font-size: 15px; }

.searching-state {
  display: flex; align-items: center; gap: 10px;
  color: #64748b; font-size: 13px;
}

.spinner {
  width: 20px; height: 20px;
  border: 2px solid #e2e8f0; border-top-color: #2563eb;
  border-radius: 50%; animation: spin .8s linear infinite; flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }

// ── Kolom kanan ───────────────────────────────────────────────
.empty-hint {
  color: #94a3b8; font-size: 13px; font-weight: 500;
  display: flex; align-items: center; gap: 8px;
  text-transform: none; letter-spacing: 0;
}

.empty-result {
  display: flex; flex-direction: column;
  align-items: center; min-height: 120px;
  color: #94a3b8; text-align: center;
  i { font-size: 32px; margin-bottom: 8px; }
  p { margin: 2px 0; font-size: 13px; }
}

.results-section .section-label { justify-content: space-between; margin-bottom: 8px; }

.results-count {
  font-size: 11px; color: #2563eb; font-weight: 600;
  background: #eff6ff; padding: 2px 8px; border-radius: 20px;
  text-transform: none; letter-spacing: 0;
}

.result-card {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 0; border-bottom: 1px solid #f1f5f9;
  &:last-child { border-bottom: none; }
  &:hover { background: #f8fafc; border-radius: 8px; }
}

.result-images { display: flex; gap: 4px; flex-shrink: 0; }

.result-thumb {
  width: 56px; height: 56px; object-fit: cover;
  border-radius: 8px; border: 1px solid #e2e8f0; cursor: zoom-in;
  &:not(:first-child) {
    display: none;
    @media (min-width: 480px) { display: block; width: 48px; height: 48px; }
  }
}

.result-info { flex: 1; min-width: 0; }
.result-name { font-weight: 600; font-size: 14px; color: #1e293b; margin-bottom: 2px; }
.result-price { font-size: 13px; font-weight: 700; color: #2563eb; margin-bottom: 3px; }
.result-meta { display: flex; gap: 8px; align-items: center; }
.result-stock { font-size: 12px; color: #64748b; }
.result-status {
  font-size: 11px; font-weight: 600; padding: 1px 6px; border-radius: 20px;
  &.active   { background: #dcfce7; color: #16a34a; }
  &.inactive { background: #fef2f2; color: #ef4444; }
}
</style>

<script>
import items from "../apis/items";
import { isMobileDevice, startDesktopCamera, snapshotFromVideo, fileToBase64 } from "../utils/cameraHelper";

export default {
  data() {
    return {
      isMobile: isMobileDevice(),
      capturedImage: null,
      searchResults: [],
      searching: false,
      shotTaken: false,
      cameraReady: false,
      cameraError: null,
      stream: null,
      showZoom: false,
      zoomImage: null,
    };
  },
  mounted() {
    if (!this.isMobile) this.initDesktopCamera();
  },
  beforeDestroy() {
    if (this.stream) this.stream.getTracks().forEach(t => t.stop());
  },
  methods: {
    async initDesktopCamera() {
      try {
        this.stream = await startDesktopCamera(this.$refs.video);
        this.cameraReady = true;
      } catch (err) {
        console.error('Webcam gagal:', err);
        this.cameraError = 'Tidak bisa mengakses kamera. Pastikan izin diberikan.';
      }
    },
    captureDesktop() {
      const img = snapshotFromVideo(this.$refs.video, this.$refs.canvas);
      this.capturedImage = img;
      this.searchItem(img);
    },
    openCamera() {
      this.$refs.fileInput.value = '';
      this.$refs.fileInput.click();
    },
    async onFileChange(e) {
      const file = e.target.files[0];
      if (!file) return;
      const img = await fileToBase64(file);
      this.capturedImage = img;
      this.searchItem(img);
    },
    async searchItem(imageData) {
      this.shotTaken  = true;
      this.searching  = true;
      this.searchResults = [];
      try {
        const response = await items.search({ image: imageData });
        const list = response.data || [];
        list.forEach(el => {
          el.image1 = el.image2 = el.image3 = '';
          if (el.image_id) {
            items.imageItem(el.image_id).then(img => { el.image1 = img; this.$forceUpdate(); });
          }
        });
        this.searchResults = list;
      } catch (err) {
        console.error('Error search:', err);
      } finally {
        this.searching = false;
      }
    },
    getImages(item) {
      return [item.image1, item.image2, item.image3].filter(Boolean);
    },
    openZoom(img) { this.zoomImage = img; this.showZoom = true; },
  },
};
</script>
