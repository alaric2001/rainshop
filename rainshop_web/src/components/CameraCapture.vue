<template>
  <div>
    <video ref="video" width="640" height="480" autoplay muted></video>
    <button @click="capture">Ambil Gambar</button>
    <canvas ref="canvas" width="640" height="480" style="display: none;"></canvas>
    <img v-if="capturedImage" :src="capturedImage" alt="Captured" width="300" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      capturedImage: null,
    };
  },
  mounted() {
    this.initCamera();
  },
  methods: {
    async initCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        this.$refs.video.srcObject = stream;
      } catch (error) {
        console.error("Error accessing webcam:", error);
        alert("Tidak bisa mengakses webcam!");
      }
    },
    capture() {
      const video = this.$refs.video;
      const canvas = this.$refs.canvas;
      const context = canvas.getContext("2d");

      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      this.capturedImage = canvas.toDataURL("image/jpeg");  // Base64 image
      this.$emit("image-captured", this.capturedImage);  // Kirim ke parent
    },
  },
  beforeDestroy() {
    if (this.$refs.video.srcObject) {
      this.$refs.video.srcObject.getTracks().forEach((track) => track.stop());
    }
  },
};
</script>