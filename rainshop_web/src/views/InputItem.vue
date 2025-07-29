<template>
  <div>
    <h1>Input Item Barang</h1>
    <CameraCapture @image-captured="handleImageCaptured" />
    <form @submit.prevent="submitItem">
      <input v-model="item_name" placeholder="Nama Barang" required />
      <input v-model="item_price" placeholder="Harga Barang" required />
      <input v-model="item_stock" placeholder="Stock Barang" required />
      <button type="submit" :disabled="!capturedImage">Simpan</button>
    </form>
  </div>
</template>

<script>
import CameraCapture from "../components/CameraCapture.vue";
import axios from "axios";

export default {
  components: { CameraCapture },
  data() {
    return {
      item_name: "",
      item_price: "",
      item_stock: "",
      capturedImage: null,
    };
  },
  methods: {
    handleImageCaptured(imageData) {
      this.capturedImage = imageData;
    },
    async submitItem() {
      try {
        const response = await axios.post("http://localhost:8000/items", {
          item_name: this.item_name,
          item_price: this.item_price,
          image: this.capturedImage,  // Base64 image
        });
        alert("Item berhasil disimpan!");
        this.resetForm();
      } catch (error) {
        console.error("Error saving item:", error);
        alert("Gagal menyimpan item!");
      }
    },
    resetForm() {
      this.itemName = "";
      this.itemDescription = "";
      this.capturedImage = null;
    },
  },
};
</script>