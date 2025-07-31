<template>
  <div>
    <b-row>
      <b-col lg="7">
          <video ref="video" width="640" height="480" autoplay muted></video>
        <canvas ref="canvas" width="640" height="480" style="display: none;"></canvas>
      </b-col>
      <b-col lg="5">
        <div style="height:300; ">
            <img v-if="capturedImage" :src="capturedImage" alt="Captured" width="300" />
        </div>
          <b-input-group class="mt-4 ml-4">
              <b-input-group-append>
                  <b-button variant="primary mr-1" @click="capture">Ambil <i class="fa fa-camera"></i></b-button>
              </b-input-group-append>
          </b-input-group>
      </b-col>
    </b-row>  
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