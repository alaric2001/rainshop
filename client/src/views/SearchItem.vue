<template>
  <div class="search-page">

    <div class="page-header">
      <h6 class="page-title"><i class="fa fa-search"></i> Cari Barang dengan Kamera</h6>
    </div>

    <!-- Kamera -->
    <div class="camera-section">
      <div class="camera-wrapper">
        <video ref="video" autoplay muted playsinline></video>
        <canvas ref="canvas" style="display:none;"></canvas>
      </div>
      <b-button
        variant="primary"
        size="lg"
        class="btn-capture w-100 mt-2"
        @click="capture"
        :disabled="!cameraReady"
      >
        <i class="fa fa-camera"></i>
        {{ cameraReady ? 'Ambil Foto & Cari' : 'Membuka kamera...' }}
      </b-button>
      <div v-if="!cameraReady && cameraError" class="camera-error">
        <i class="fa fa-exclamation-triangle"></i> {{ cameraError }}
      </div>
    </div>

    <!-- Loading -->
    <div v-if="searching" class="searching-state">
      <div class="spinner"></div>
      <p>Mencari barang serupa...</p>
    </div>

    <!-- Hasil Pencarian -->
    <div v-if="searchResults.length && !searching" class="results-section">
      <div class="results-header">
        <span class="results-title">Hasil Pencarian</span>
        <span class="results-count">{{ searchResults.length }} barang ditemukan</span>
      </div>

      <div class="results-list">
        <div
          v-for="item in searchResults"
          :key="item.item_id"
          class="result-card"
        >
          <!-- Gambar item (tampilkan yang tersedia) -->
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

          <!-- Info item -->
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

    <!-- Kosong setelah foto diambil -->
    <div v-if="shotTaken && !searching && searchResults.length === 0" class="empty-result">
      <i class="fa fa-search"></i>
      <p>Tidak ada barang yang cocok</p>
      <p class="text-muted small">Coba arahkan kamera lebih dekat ke barang</p>
    </div>

    <!-- Modal zoom -->
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

.page-header {
  padding: 10px 4px 8px;
}

.page-title {
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  i { margin-right: 6px; color: #2563eb; }
}

// ── Kamera ────────────────────────────────────────────────────
.camera-section {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 12px;
  margin-bottom: 10px;
  box-shadow: 0 1px 3px rgba(0,0,0,.05);
}

.camera-wrapper {
  width: 100%;
  background: #0f172a;
  border-radius: 8px;
  overflow: hidden;
  position: relative;

  video {
    width: 100%;
    height: auto;
    max-height: 280px;
    object-fit: cover;
    display: block;
  }
}

.btn-capture {
  font-weight: 700;
  font-size: 16px;
  letter-spacing: .03em;
}

.camera-error {
  margin-top: 8px;
  color: #ef4444;
  font-size: 13px;
  text-align: center;
}

// ── Loading ───────────────────────────────────────────────────
.searching-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px;
  color: #64748b;

  p { margin: 8px 0 0; font-size: 14px; }
}

.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid #e2e8f0;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin .8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

// ── Hasil ─────────────────────────────────────────────────────
.results-section {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,.05);
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.results-title {
  font-size: 12px;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: .05em;
}

.results-count {
  font-size: 12px;
  color: #2563eb;
  font-weight: 600;
  background: #eff6ff;
  padding: 2px 8px;
  border-radius: 20px;
}

.result-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-bottom: 1px solid #f1f5f9;
  transition: background .15s;

  &:last-child { border-bottom: none; }
  &:hover { background: #f8fafc; }
}

.result-images {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}

.result-thumb {
  width: 56px;
  height: 56px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  cursor: zoom-in;

  // di mobile cukup 1 gambar besar
  &:not(:first-child) {
    display: none;

    @media (min-width: 480px) {
      display: block;
      width: 48px;
      height: 48px;
    }
  }
}

.result-info {
  flex: 1;
  min-width: 0;
}

.result-name {
  font-weight: 600;
  font-size: 15px;
  color: #1e293b;
  line-height: 1.3;
  margin-bottom: 3px;
}

.result-price {
  font-size: 14px;
  font-weight: 700;
  color: #2563eb;
  margin-bottom: 4px;
}

.result-meta {
  display: flex;
  gap: 8px;
  align-items: center;
}

.result-stock {
  font-size: 12px;
  color: #64748b;
}

.result-status {
  font-size: 11px;
  font-weight: 600;
  padding: 1px 6px;
  border-radius: 20px;

  &.active   { background: #dcfce7; color: #16a34a; }
  &.inactive { background: #fef2f2; color: #ef4444; }
}

// ── Kosong ────────────────────────────────────────────────────
.empty-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  color: #94a3b8;
  text-align: center;

  i { font-size: 40px; margin-bottom: 12px; }
  p { margin: 2px 0; font-size: 14px; }
}
</style>

<script>
import items from "../apis/items";

export default {
  components: {},
  data() {
    return {
      searchResults: [],
      searching: false,
      shotTaken: false,
      cameraReady: false,
      cameraError: null,
      showZoom: false,
      zoomImage: null,
    };
  },
  mounted() {
    this.initCamera();
  },
  beforeDestroy() {
    this.stopCamera();
  },
  methods: {
    async initCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: { ideal: 'environment' } } // kamera belakang di HP
        });
        this.$refs.video.srcObject = stream;
        this.cameraReady = true;
      } catch (err) {
        console.error('Kamera gagal:', err);
        this.cameraError = 'Tidak bisa mengakses kamera. Pastikan izin kamera sudah diberikan.';
      }
    },
    stopCamera() {
      const video = this.$refs.video;
      if (video && video.srcObject) {
        video.srcObject.getTracks().forEach(t => t.stop());
      }
    },
    async capture() {
      const video = this.$refs.video;
      const canvas = this.$refs.canvas;
      canvas.width  = video.videoWidth  || 480;
      canvas.height = video.videoHeight || 360;
      canvas.getContext('2d').drawImage(video, 0, 0);
      const imageData = canvas.toDataURL('image/jpeg');
      await this.searchItem(imageData);
    },
    async searchItem(imageData) {
      this.shotTaken = true;
      this.searching = true;
      this.searchResults = [];
      try {
        const response = await items.search({ image: imageData });
        const list = response.data || [];
        // Muat gambar untuk setiap item
        list.forEach(el => {
          el.image1 = el.image2 = el.image3 = '';
          if (el.image_id) {
            items.imageItem(el.image_id).then(img => { el.image1 = img; this.$forceUpdate(); });
          }
        });
        this.searchResults = list;
      } catch (error) {
        console.error('Error search:', error);
      } finally {
        this.searching = false;
      }
    },
    getImages(item) {
      return [item.image1, item.image2, item.image3].filter(Boolean);
    },
    openZoom(img) {
      this.zoomImage = img;
      this.showZoom = true;
    },
  },
};
</script>
