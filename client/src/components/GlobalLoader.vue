<template>
  <transition name="loader-fade">
    <div v-if="loading.active" class="loader-backdrop">
      <div class="loader-card">
        <div class="loader-ring">
          <div></div><div></div><div></div><div></div>
        </div>
        <p v-if="loading.message" class="loader-msg">{{ loading.message }}</p>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.loader-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(241, 245, 249, 0.82);
  backdrop-filter: blur(3px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
}

.loader-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  background: #fff;
  border-radius: 16px;
  padding: 32px 40px;
  box-shadow: 0 8px 32px rgba(0,0,0,.12);
}

/* Spinner ring */
.loader-ring {
  position: relative;
  width: 52px;
  height: 52px;
}

.loader-ring div {
  box-sizing: border-box;
  position: absolute;
  inset: 0;
  border: 5px solid transparent;
  border-radius: 50%;
  animation: ring-spin 1s cubic-bezier(.5,0,.5,1) infinite;
}

.loader-ring div:nth-child(1) { border-top-color: #2563eb; animation-delay: -.45s; }
.loader-ring div:nth-child(2) { border-top-color: #3b82f6; animation-delay: -.3s;  }
.loader-ring div:nth-child(3) { border-top-color: #60a5fa; animation-delay: -.15s; }
.loader-ring div:nth-child(4) { border-top-color: #93c5fd; }

@keyframes ring-spin {
  0%   { transform: rotate(0deg);   }
  100% { transform: rotate(360deg); }
}

/* Message */
.loader-msg {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  text-align: center;
  max-width: 200px;
}

/* Transition */
.loader-fade-enter-active,
.loader-fade-leave-active { transition: opacity .2s ease; }
.loader-fade-enter,
.loader-fade-leave-to      { opacity: 0; }
</style>

<script>
import { mapState } from 'vuex';

export default {
  computed: {
    ...mapState(['loading']),
  },
};
</script>
