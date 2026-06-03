<template>
  <div class="camera-capture3">

    <!-- ── DESKTOP: satu webcam, tiga tombol snapshot ───────── -->
    <template v-if="!isMobile">
      <div class="video-box">
        <video ref="video" autoplay muted playsinline></video>
        <canvas ref="canvas" style="display:none;"></canvas>
      </div>
      <div class="btn-row">
        <b-button variant="primary" size="sm" @click="captureDesktop(0)">
          <i class="fa fa-camera"></i> Foto #1
        </b-button>
        <b-button variant="primary" size="sm" @click="captureDesktop(1)">
          <i class="fa fa-camera"></i> Foto #2
        </b-button>
        <b-button variant="primary" size="sm" @click="captureDesktop(2)">
          <i class="fa fa-camera"></i> Foto #3
        </b-button>
      </div>
      <!-- Preview thumbnail desktop -->
      <div class="thumb-row" v-if="anyCaptured">
        <img v-for="(img, i) in captured" :key="i" :src="img || ''" class="thumb" :alt="'Foto '+(i+1)" />
      </div>
    </template>

    <!-- ── MOBILE: tiga slot preview + tiga tombol kamera ───── -->
    <template v-else>
      <div class="preview-grid">
        <div
          v-for="(img, idx) in captured"
          :key="idx"
          class="preview-slot"
          @click="openCamera(idx)"
        >
          <img v-if="img" :src="img" class="slot-img" alt />
          <div v-else class="slot-placeholder">
            <i class="fa fa-camera"></i>
            <span>Foto #{{ idx + 1 }}</span>
          </div>
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
      <div class="btn-row">
        <b-button
          v-for="(img, idx) in captured"
          :key="idx"
          variant="primary"
          size="sm"
          @click="openCamera(idx)"
        >
          <i class="fa fa-camera"></i>
          {{ img ? '↺ #' + (idx + 1) : 'Foto #' + (idx + 1) }}
        </b-button>
      </div>
    </template>

  </div>
</template>

<style scoped>
.camera-capture3 { width: 100%; }

/* Desktop */
.video-box {
  width: 100%; aspect-ratio: 16/9;
  background: #0f172a; border-radius: 8px; overflow: hidden;
}
.video-box video { width: 100%; height: 100%; object-fit: cover; display: block; }
.thumb-row { display: flex; gap: 6px; margin-top: 6px; }
.thumb {
  width: 72px; height: 54px; object-fit: cover;
  border-radius: 6px; border: 1px solid #e2e8f0;
}

/* Mobile */
.preview-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 6px; margin-bottom: 8px; }
.preview-slot {
  aspect-ratio: 1; background: #0f172a; border-radius: 8px; overflow: hidden;
  cursor: pointer; display: flex; align-items: center; justify-content: center;
}
.slot-img { width: 100%; height: 100%; object-fit: cover; display: block; }
.slot-placeholder {
  display: flex; flex-direction: column; align-items: center; gap: 4px;
  color: #64748b; font-size: 11px;
}
.slot-placeholder i { font-size: 22px; color: #334155; }

/* Shared */
.btn-row { display: flex; gap: 6px; }
.btn-row .btn { flex: 1; font-size: 12px; }
</style>

<script>
import { isMobileDevice, startDesktopCamera, snapshotFromVideo, fileToBase64 } from '../utils/cameraHelper';

export default {
  data() {
    return {
      isMobile: isMobileDevice(),
      captured: [null, null, null],
      activeIdx: 0,
      stream: null,
    };
  },
  computed: {
    anyCaptured() { return this.captured.some(Boolean); },
  },
  mounted() {
    if (!this.isMobile) {
      startDesktopCamera(this.$refs.video)
        .then(s => { this.stream = s; })
        .catch(err => console.error('Webcam gagal:', err));
    }
  },
  methods: {
    captureDesktop(idx) {
      const img = snapshotFromVideo(this.$refs.video, this.$refs.canvas);
      this.$set(this.captured, idx, img);
      const events = ['image-captured', 'image2-captured', 'image3-captured'];
      this.$emit(events[idx], img);
    },
    openCamera(idx) {
      this.activeIdx = idx;
      this.$refs.fileInput.value = '';
      this.$refs.fileInput.click();
    },
    async onFileChange(e) {
      const file = e.target.files[0];
      if (!file) return;
      const img = await fileToBase64(file);
      this.$set(this.captured, this.activeIdx, img);
      const events = ['image-captured', 'image2-captured', 'image3-captured'];
      this.$emit(events[this.activeIdx], img);
    },
  },
  beforeDestroy() {
    if (this.stream) this.stream.getTracks().forEach(t => t.stop());
  },
};
</script>
