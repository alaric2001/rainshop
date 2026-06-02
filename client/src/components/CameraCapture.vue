<template>
  <div class="camera-capture">
    <div class="video-box">
      <video ref="video" autoplay muted playsinline></video>
      <canvas ref="canvas" style="display:none;"></canvas>
    </div>
    <div class="capture-row">
      <img v-if="capturedImage" :src="capturedImage" class="preview-thumb" alt="Preview" />
      <b-button variant="primary" class="btn-ambil" @click="capture">
        <i class="fa fa-camera"></i> Ambil Foto
      </b-button>
    </div>
  </div>
</template>

<style scoped>
.camera-capture { width: 100%; }

.video-box {
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #0f172a;
  border-radius: 8px;
  overflow: hidden;
}

.video-box video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.capture-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 8px;
}

.btn-ambil { flex-shrink: 0; }

.preview-thumb {
  height: 48px;
  width: 72px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}
</style>

<script>
export default {
  data() {
    return { capturedImage: null };
  },
  mounted() {
    navigator.mediaDevices.getUserMedia({
      video: { facingMode: { ideal: 'environment' }, aspectRatio: { ideal: 16/9 } }
    })
      .then(stream => {
        this.$store.commit('setStream', stream);
        this.$refs.video.srcObject = stream;
      })
      .catch(err => console.error('Webcam access denied:', err));
  },
  methods: {
    capture() {
      const video  = this.$refs.video;
      const canvas = this.$refs.canvas;
      canvas.width  = video.videoWidth  || 1280;
      canvas.height = video.videoHeight || 720;
      canvas.getContext('2d').drawImage(video, 0, 0);
      this.capturedImage = canvas.toDataURL('image/jpeg');
      this.$emit('image-captured', this.capturedImage);
    },
  },
  beforeDestroy() {
    const v = this.$refs.video;
    if (v && v.srcObject) v.srcObject.getTracks().forEach(t => t.stop());
  },
};
</script>
