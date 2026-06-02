<template>
  <div class="camera-capture3">
    <div class="video-box">
      <video ref="video" autoplay muted playsinline></video>
      <canvas ref="canvas" style="display:none;"></canvas>
    </div>
    <div class="btn-row">
      <b-button variant="primary" size="sm" @click="capture">
        <i class="fa fa-camera"></i> Foto #1
      </b-button>
      <b-button variant="primary" size="sm" @click="capture2">
        <i class="fa fa-camera"></i> Foto #2
      </b-button>
      <b-button variant="primary" size="sm" @click="capture3">
        <i class="fa fa-camera"></i> Foto #3
      </b-button>
    </div>
  </div>
</template>

<style scoped>
.camera-capture3 { width: 100%; }

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

.btn-row {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.btn-row .btn { flex: 1; }
</style>

<script>
export default {
  data() {
    return {
      capturedImage:  null,
      capturedImage2: null,
      capturedImage3: null,
    };
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
    _snap() {
      const video  = this.$refs.video;
      const canvas = this.$refs.canvas;
      canvas.width  = video.videoWidth  || 1280;
      canvas.height = video.videoHeight || 720;
      canvas.getContext('2d').drawImage(video, 0, 0);
      return canvas.toDataURL('image/jpeg');
    },
    capture()  { this.capturedImage  = this._snap(); this.$emit('image-captured',  this.capturedImage);  },
    capture2() { this.capturedImage2 = this._snap(); this.$emit('image2-captured', this.capturedImage2); },
    capture3() { this.capturedImage3 = this._snap(); this.$emit('image3-captured', this.capturedImage3); },
  },
  beforeDestroy() {
    const v = this.$refs.video;
    if (v && v.srcObject) v.srcObject.getTracks().forEach(t => t.stop());
  },
};
</script>
