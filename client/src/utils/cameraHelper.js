/**
 * Deteksi perangkat mobile (Android / iOS).
 * Desktop/Laptop mengembalikan false.
 */
export function isMobileDevice() {
  const ua = navigator.userAgent;
  // Cakup iPad yang melaporkan diri sebagai "Macintosh" di user agent modern
  const isIpad = navigator.maxTouchPoints > 1 && /Macintosh/i.test(ua);
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(ua) || isIpad;
}

/**
 * Mulai webcam di desktop — mengembalikan stream.
 * Hanya dipanggil saat bukan mobile.
 */
export async function startDesktopCamera(videoEl) {
  const stream = await navigator.mediaDevices.getUserMedia({
    video: { facingMode: { ideal: 'environment' }, aspectRatio: { ideal: 16 / 9 } }
  });
  videoEl.srcObject = stream;
  return stream;
}

/**
 * Ambil snapshot dari elemen <video> → base64 JPEG.
 */
export function snapshotFromVideo(videoEl, canvasEl) {
  canvasEl.width  = videoEl.videoWidth  || 1280;
  canvasEl.height = videoEl.videoHeight || 720;
  canvasEl.getContext('2d').drawImage(videoEl, 0, 0);
  return canvasEl.toDataURL('image/jpeg');
}

/**
 * Baca file dari <input type="file"> → base64 JPEG (Promise).
 */
export function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload  = e => resolve(e.target.result);
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}
