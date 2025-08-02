<template>
  <div>
    <b-row class="justify-content-center mb-2">
        <video ref="video" width="480" height="360" autoplay muted></video>
        <canvas ref="canvas" width="480" height="360" style="display: none;"></canvas>
    </b-row>
    <b-row>
      <b-col lg="4">
          <b-input-group>
              <b-input-group-prepend><label class="text-right">Gambar#1</label></b-input-group-prepend>
              <b-input-group-append>
                  <b-button variant="primary mr-1" @click="capture">Ambil <i class="fa fa-camera"></i></b-button>
              </b-input-group-append>
          </b-input-group>
        <img v-if="capturedImage" :src="capturedImage" alt="Captured#1" width="300" />
      </b-col>
      <b-col lg="4">
          <b-input-group>
              <b-input-group-prepend><label class="text-right">Gambar#2</label></b-input-group-prepend>
              <b-input-group-append>
                  <b-button variant="primary mr-1" @click="capture2">Ambil <i class="fa fa-camera"></i></b-button>
              </b-input-group-append>
          </b-input-group>
        <img v-if="capturedImage2" :src="capturedImage2" alt="Captured#1" width="300" />
      </b-col>
      <b-col lg="4">
          <b-input-group>
              <b-input-group-prepend><label class="text-right">Gambar#3</label></b-input-group-prepend>
              <b-input-group-append>
                  <b-button variant="primary mr-1" @click="capture3">Ambil <i class="fa fa-camera"></i></b-button>
              </b-input-group-append>
          </b-input-group>
        <img v-if="capturedImage3" :src="capturedImage3" alt="Captured#1" width="300" />
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      capturedImage: null,
      capturedImage2: null,
      capturedImage3: null,
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
    capture2() {
      const video = this.$refs.video;
      const canvas = this.$refs.canvas;
      const context = canvas.getContext("2d");

      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      this.capturedImage2 = canvas.toDataURL("image/jpeg");  // Base64 image
      this.$emit("image2-captured", this.capturedImage2);  // Kirim ke parent
    },
    capture3() {
      const video = this.$refs.video;
      const canvas = this.$refs.canvas;
      const context = canvas.getContext("2d");

      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      this.capturedImage3 = canvas.toDataURL("image/jpeg");  // Base64 image
      this.$emit("image3-captured", this.capturedImage3);  // Kirim ke parent
    },
  },
  beforeDestroy() {
    if (this.$refs.video.srcObject) {
      this.$refs.video.srcObject.getTracks().forEach((track) => track.stop());
    }
  },
};
</script>