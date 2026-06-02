<template>
  <div class="camera-capture2">
    <div class="video-box">
      <video ref="video" autoplay muted playsinline></video>
      <canvas ref="canvas" style="display:none;"></canvas>
    </div>
    <b-button variant="primary" class="mt-2 w-100" @click="capture">
      <i class="fa fa-camera"></i> Ambil Foto
    </b-button>
  </div>
</template>

<style scoped>
.camera-capture2 { width: 100%; }

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
