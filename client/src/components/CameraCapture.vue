<template>
  <div class="camera-capture">

    <!-- ── DESKTOP: webcam live preview ────────────────────── -->
    <template v-if="!isMobile">
      <div class="video-box">
        <video ref="video" autoplay muted playsinline></video>
        <canvas ref="canvas" style="display:none;"></canvas>
      </div>
      <div class="capture-row">
        <img v-if="capturedImage" :src="capturedImage" class="preview-thumb" alt="Preview" />
        <b-button variant="primary" class="btn-ambil" @click="captureDesktop">
          <i class="fa fa-camera"></i> Ambil Foto
        </b-button>
      </div>
    </template>

    <!-- ── MOBILE: kamera bawaan via file input ─────────────── -->
    <template v-else>
      <div class="preview-box" @click="openCamera">
        <img v-if="capturedImage" :src="capturedImage" class="preview-img" alt="Foto" />
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
      <b-button variant="primary" class="w-100 mt-2" @click="openCamera">
        <i class="fa fa-camera"></i> Ambil Foto
      </b-button>
    </template>

  </div>
</template>

<style scoped>
.camera-capture { width: 100%; }

/* Desktop */
.video-box {
  width: 100%; aspect-ratio: 16/9;
  background: #0f172a; border-radius: 8px; overflow: hidden;
}
.video-box video { width: 100%; height: 100%; object-fit: cover; display: block; }
.capture-row { display: flex; align-items: center; gap: 10px; margin-top: 8px; }
.btn-ambil { flex-shrink: 0; }
.preview-thumb {
  height: 48px; width: 72px; object-fit: cover;
  border-radius: 6px; border: 1px solid #e2e8f0;
}

/* Mobile */
.preview-box {
  width: 100%; aspect-ratio: 16/9;
  background: #0f172a; border-radius: 8px; overflow: hidden;
  cursor: pointer; display: flex; align-items: center; justify-content: center;
}
.preview-img { width: 100%; height: 100%; object-fit: cover; display: block; }
.preview-placeholder {
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  color: #64748b; font-size: 13px;
}
.preview-placeholder i { font-size: 36px; color: #334155; }
</style>

<script>
import { isMobileDevice, startDesktopCamera, snapshotFromVideo, fileToBase64 } from '../utils/cameraHelper';

export default {
  data() {
    return {
      isMobile: isMobileDevice(),
      capturedImage: null,
      stream: null,
    };
  },
  mounted() {
    if (!this.isMobile) {
      startDesktopCamera(this.$refs.video)
        .then(s => { this.stream = s; })
        .catch(err => console.error('Webcam gagal:', err));
    }
  },
  methods: {
    captureDesktop() {
      const img = snapshotFromVideo(this.$refs.video, this.$refs.canvas);
      this.capturedImage = img;
      this.$emit('image-captured', img);
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
      this.$emit('image-captured', img);
    },
  },
  beforeDestroy() {
    if (this.stream) this.stream.getTracks().forEach(t => t.stop());
  },
};
</script>
